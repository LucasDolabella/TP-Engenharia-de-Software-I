from app.database import db
from app.models.penalidade import Penalidade, StatusPenalidade
from app.external.payment_service import PaymentService
from app.external.email_service import EmailService


class PenalidadeService:

    @staticmethod
    def listar_por_usuario(usuario_id: str) -> list:
        return Penalidade.listar_por_usuario(usuario_id)

    @staticmethod
    def obter(penalidade_id: str) -> Penalidade:
        penalidade = Penalidade.query.get(penalidade_id)
        if not penalidade:
            raise ValueError("Penalidade não encontrada.")
        return penalidade

    @staticmethod
    def processar_pagamento(penalidade_id: str, usuario_id: str, metodo: str) -> dict:
        penalidade = PenalidadeService.obter(penalidade_id)
        if penalidade.usuario_id != usuario_id:
            raise PermissionError("Sem permissão para pagar esta penalidade.")
        if penalidade.status != StatusPenalidade.PENDENTE.value:
            raise ValueError("Penalidade não está pendente.")

        resultado = PaymentService.processar(penalidade.valor_multa, metodo)

        if resultado["status"] == "aprovado":
            penalidade.confirmar_pagamento()
            EmailService.enviar_comprovante_pagamento(penalidade)
            return {"sucesso": True, "mensagem": "Pagamento aprovado. Acesso desbloqueado."}
        elif resultado["status"] == "timeout":
            penalidade.status = StatusPenalidade.PENDENTE.value
            db.session.commit()
            return {"sucesso": False, "mensagem": "Timeout no pagamento. Verificação pendente."}
        else:
            return {"sucesso": False, "mensagem": "Pagamento recusado. Bloqueio mantido."}