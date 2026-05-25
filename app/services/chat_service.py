from app.database import db
from app.models.mensagem import Mensagem
from app.models.emprestimo import Emprestimo
from app.models.notificacao import Notificacao, TipoNotificacao


class ChatService:

    @staticmethod
    def listar_mensagens(emprestimo_id: str, usuario_id: str) -> list:
        emprestimo = Emprestimo.query.get(emprestimo_id)
        if not emprestimo:
            raise ValueError("Empréstimo não encontrado.")
        if usuario_id not in (emprestimo.dono_id, emprestimo.solicitante_id):
            raise PermissionError("Acesso não autorizado ao chat.")
        return Mensagem.listar_por_emprestimo(emprestimo_id)

    @staticmethod
    def enviar_mensagem(emprestimo_id: str, remetente, conteudo: str) -> Mensagem:
        emprestimo = Emprestimo.query.get(emprestimo_id)
        if not emprestimo:
            raise ValueError("Empréstimo não encontrado.")
        if remetente.id not in (emprestimo.dono_id, emprestimo.solicitante_id):
            raise PermissionError("Acesso não autorizado ao chat.")

        destinatario_id = (
            emprestimo.solicitante_id
            if remetente.id == emprestimo.dono_id
            else emprestimo.dono_id
        )
        from app.models.usuario import Usuario
        destinatario = Usuario.query.get(destinatario_id)

        mensagem = Mensagem()
        mensagem.enviar(remetente, destinatario, emprestimo, conteudo)
        db.session.add(mensagem)

        notif = Notificacao()
        notif.enviar(destinatario, TipoNotificacao.NOVA_MENSAGEM.value, emprestimo)
        db.session.add(notif)
        db.session.commit()

        return mensagem

    @staticmethod
    def marcar_como_lidas(emprestimo_id: str, usuario_id: str) -> None:
        mensagens = Mensagem.query.filter_by(
            emprestimo_id=emprestimo_id, destinatario_id=usuario_id, lida=False
        ).all()
        for mensagem in mensagens:
            mensagem.lida = True
        db.session.commit()