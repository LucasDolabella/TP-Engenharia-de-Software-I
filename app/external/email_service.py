import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Stub do sistema externo de e-mail. Em produção, integrar com SMTP/SendGrid."""

    @staticmethod
    def enviar_aviso_prazo_vencido(emprestimo) -> bool:
        destinatario = emprestimo.dono.email
        jogo = emprestimo.jogo.nome
        logger.info(f"[EMAIL] Para: {destinatario} | Assunto: Prazo vencido para '{jogo}'")
        logger.info(f"[EMAIL] O jogo '{jogo}' deveria ter sido devolvido. Confirme a devolução.")
        return True

    @staticmethod
    def enviar_confirmacao_devolucao(emprestimo) -> bool:
        destinatario = emprestimo.solicitante.email
        jogo = emprestimo.jogo.nome
        logger.info(f"[EMAIL] Para: {destinatario} | Assunto: Devolução confirmada para '{jogo}'")
        return True

    @staticmethod
    def enviar_aviso_penalidade(emprestimo, penalidade) -> bool:
        destinatario = emprestimo.solicitante.email
        jogo = emprestimo.jogo.nome
        valor = penalidade.valor_multa
        logger.info(f"[EMAIL] Para: {destinatario} | Assunto: Penalidade de R${valor:.2f} aplicada por '{jogo}'")
        return True

    @staticmethod
    def enviar_comprovante_pagamento(penalidade) -> bool:
        destinatario = penalidade.usuario.email
        valor = penalidade.valor_multa
        logger.info(f"[EMAIL] Para: {destinatario} | Assunto: Comprovante de pagamento de R${valor:.2f}")
        return True