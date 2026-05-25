from datetime import datetime
from app.database import db
from app.models.emprestimo import Emprestimo, StatusEmprestimo
from app.models.jogo import StatusJogo
from app.models.notificacao import Notificacao, TipoNotificacao
from app.models.penalidade import Penalidade
from app.external.email_service import EmailService


class EmprestimoService:

    @staticmethod
    def solicitar(solicitante, jogo, data_prazo_str: str) -> Emprestimo:
        data_prazo = datetime.fromisoformat(data_prazo_str)
        emprestimo = Emprestimo()
        emprestimo.solicitar(solicitante, jogo, data_prazo)
        jogo.atualizar_status(StatusJogo.EMPRESTADO.value)
        db.session.add(emprestimo)
        db.session.commit()

        notif = Notificacao()
        notif.enviar(jogo.dono, TipoNotificacao.SOLICITACAO_EMPRESTIMO.value, emprestimo)
        db.session.add(notif)
        db.session.commit()

        return emprestimo

    @staticmethod
    def listar_por_usuario(usuario_id: str) -> list:
        como_solicitante = Emprestimo.query.filter_by(solicitante_id=usuario_id).all()
        como_dono = Emprestimo.query.filter_by(dono_id=usuario_id).all()
        vistos = set()
        resultado = []
        for e in como_solicitante + como_dono:
            if e.id not in vistos:
                vistos.add(e.id)
                resultado.append(e)
        return resultado

    @staticmethod
    def obter(emprestimo_id: str) -> Emprestimo:
        emprestimo = Emprestimo.query.get(emprestimo_id)
        if not emprestimo:
            raise ValueError("Empréstimo não encontrado.")
        return emprestimo

    @staticmethod
    def confirmar_devolucao(emprestimo_id: str, usuario_id: str) -> Emprestimo:
        emprestimo = EmprestimoService.obter(emprestimo_id)
        if emprestimo.dono_id != usuario_id:
            raise PermissionError("Apenas o dono pode confirmar a devolução.")
        if emprestimo.status != StatusEmprestimo.ATIVO.value:
            raise ValueError("Empréstimo não está ativo.")
        emprestimo.confirmar_devolucao()
        db.session.commit()

        notif = Notificacao()
        notif.enviar(emprestimo.solicitante, TipoNotificacao.DEVOLUCAO_CONFIRMADA.value, emprestimo)
        db.session.add(notif)
        db.session.commit()

        EmailService.enviar_confirmacao_devolucao(emprestimo)
        return emprestimo

    @staticmethod
    def registrar_nao_devolucao(emprestimo_id: str, usuario_id: str) -> Emprestimo:
        emprestimo = EmprestimoService.obter(emprestimo_id)
        if emprestimo.dono_id != usuario_id:
            raise PermissionError("Apenas o dono pode registrar não devolução.")
        if emprestimo.status != StatusEmprestimo.ATIVO.value:
            raise ValueError("Empréstimo não está ativo.")

        penalidade = Penalidade()
        penalidade.aplicar(emprestimo.solicitante, emprestimo)
        db.session.add(penalidade)
        db.session.commit()

        notif = Notificacao()
        notif.enviar(emprestimo.solicitante, TipoNotificacao.PENALIDADE_APLICADA.value, emprestimo)
        db.session.add(notif)
        db.session.commit()

        EmailService.enviar_aviso_penalidade(emprestimo, penalidade)
        return emprestimo

    @staticmethod
    def cancelar(emprestimo_id: str, usuario_id: str) -> Emprestimo:
        emprestimo = EmprestimoService.obter(emprestimo_id)
        if emprestimo.solicitante_id != usuario_id and emprestimo.dono_id != usuario_id:
            raise PermissionError("Sem permissão para cancelar este empréstimo.")
        if emprestimo.status != StatusEmprestimo.ATIVO.value:
            raise ValueError("Empréstimo não está ativo.")
        emprestimo.cancelar()
        db.session.commit()
        return emprestimo

    @staticmethod
    def verificar_prazos_vencidos() -> None:
        ativos = Emprestimo.query.filter_by(status=StatusEmprestimo.ATIVO.value).all()
        for emprestimo in ativos:
            if emprestimo.verificar_atraso():
                EmailService.enviar_aviso_prazo_vencido(emprestimo)
                notif = Notificacao()
                notif.enviar(emprestimo.dono, TipoNotificacao.PRAZO_VENCIDO.value, emprestimo)
                db.session.add(notif)
        db.session.commit()