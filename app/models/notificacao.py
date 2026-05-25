import uuid
from datetime import datetime
from enum import Enum
from app.database import db


class TipoNotificacao(str, Enum):
    SOLICITACAO_EMPRESTIMO = "SOLICITACAO_EMPRESTIMO"
    PRAZO_VENCIDO = "PRAZO_VENCIDO"
    DEVOLUCAO_CONFIRMADA = "DEVOLUCAO_CONFIRMADA"
    NOVA_MENSAGEM = "NOVA_MENSAGEM"
    PENALIDADE_APLICADA = "PENALIDADE_APLICADA"


class Notificacao(db.Model):
    __tablename__ = "notificacoes"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destinatario_id = db.Column(db.String(36), db.ForeignKey("usuarios.id"), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    lida = db.Column(db.Boolean, default=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    emprestimo_id = db.Column(db.String(36), db.ForeignKey("emprestimos.id"), nullable=True)

    destinatario = db.relationship("Usuario", back_populates="notificacoes")
    emprestimo = db.relationship("Emprestimo", back_populates="notificacoes")

    def enviar(self, destinatario, tipo: str, emprestimo=None) -> None:
        self.destinatario_id = destinatario.id
        self.tipo = tipo
        self.mensagem = self._gerar_mensagem(tipo, emprestimo)
        self.emprestimo_id = emprestimo.id if emprestimo else None
        self.lida = False

    def marcar_como_lida(self) -> None:
        self.lida = True
        db.session.commit()

    @staticmethod
    def listar_por_usuario(usuario_id: str) -> list:
        return (
            Notificacao.query.filter_by(destinatario_id=usuario_id)
            .order_by(Notificacao.data_envio.desc())
            .all()
        )

    def cancelar(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def registrar(self) -> None:
        db.session.add(self)
        db.session.commit()

    def _gerar_mensagem(self, tipo: str, emprestimo=None) -> str:
        jogo_nome = emprestimo.jogo.nome if emprestimo and emprestimo.jogo else "jogo"
        mensagens = {
            TipoNotificacao.SOLICITACAO_EMPRESTIMO.value: f"Nova solicitação de empréstimo para '{jogo_nome}'.",
            TipoNotificacao.PRAZO_VENCIDO.value: f"O prazo de devolução de '{jogo_nome}' venceu.",
            TipoNotificacao.DEVOLUCAO_CONFIRMADA.value: f"A devolução de '{jogo_nome}' foi confirmada.",
            TipoNotificacao.NOVA_MENSAGEM.value: f"Você recebeu uma nova mensagem sobre '{jogo_nome}'.",
            TipoNotificacao.PENALIDADE_APLICADA.value: f"Uma penalidade foi aplicada pelo atraso na devolução de '{jogo_nome}'.",
        }
        return mensagens.get(tipo, "Você tem uma nova notificação.")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "destinatario_id": self.destinatario_id,
            "mensagem": self.mensagem,
            "tipo": self.tipo,
            "lida": self.lida,
            "data_envio": self.data_envio.isoformat() if self.data_envio else None,
            "emprestimo_id": self.emprestimo_id,
        }