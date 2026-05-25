import logging

logger = logging.getLogger(__name__)


class PaymentService:
    """Stub do sistema externo de pagamento. Em produção, integrar com Stripe/PagSeguro."""

    @staticmethod
    def processar(valor: float, metodo: str) -> dict:
        logger.info(f"[PAGAMENTO] Processando R${valor:.2f} via {metodo}")
        # Simulação: sempre aprova em ambiente de desenvolvimento
        return {"status": "aprovado", "transacao_id": "TXN-SIMULADO-001"}