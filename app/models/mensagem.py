import uuid
from datetime import datetime
from app.database import db


class Mensagem(db.Model):
    __tablename__ = "mensagens"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    remetente_id = db.Column(db.String(36), db.ForeignKey("usuarios.id"), nullable=False)
    destinatario_id = db.Column(db.String(36), db.ForeignKey("usuarios.id"), nullable=False)
    emprestimo_id = db.Column(db.String(36), db.ForeignKey("emprestimos.id"), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    lida = db.Column(db.Boolean, default=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)

    remetente = db.relationship("Usuario", foreign_keys=[remetente_id])
    destinatario = db.relationship("Usuario", foreign_keys=[destinatario_id])
    emprestimo = db.relationship("Emprestimo", back_populates="mensagens")

    def enviar(self, remetente, destinatario, emprestimo, conteudo: str) -> None:
        if not self._validar_conteudo(conteudo):
            raise ValueError("Mensagem não pode ser vazia.")
        self.remetente_id = remetente.id
        self.destinatario_id = destinatario.id
        self.emprestimo_id = emprestimo.id
        self.conteudo = conteudo
        self.lida = False

    def marcar_como_lida(self) -> None:
        self.lida = True
        db.session.commit()

    @staticmethod
    def listar_por_emprestimo(emprestimo_id: str) -> list:
        return Mensagem.query.filter_by(emprestimo_id=emprestimo_id).order_by(Mensagem.data_envio).all()

    def excluir(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def _validar_conteudo(self, conteudo: str) -> bool:
        return bool(conteudo and conteudo.strip())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "remetente_id": self.remetente_id,
            "remetente_nome": self.remetente.nome if self.remetente else None,
            "destinatario_id": self.destinatario_id,
            "emprestimo_id": self.emprestimo_id,
            "conteudo": self.conteudo,
            "lida": self.lida,
            "data_envio": self.data_envio.isoformat() if self.data_envio else None,
        }