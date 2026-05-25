import uuid
from datetime import datetime
from enum import Enum
from app.database import db

MULTA_POR_DIA = 5.0


class StatusPenalidade(str, Enum):
    PENDENTE = "PENDENTE"
    PAGA = "PAGA"
    CANCELADA = "CANCELADA"


class Penalidade(db.Model):
    __tablename__ = "penalidades"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = db.Column(db.String(36), db.ForeignKey("usuarios.id"), nullable=False)
    emprestimo_id = db.Column(db.String(36), db.ForeignKey("emprestimos.id"), nullable=False)
    valor_multa = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), nullable=False, default=StatusPenalidade.PENDENTE.value)
    data_aplicacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_pagamento = db.Column(db.DateTime, nullable=True)

    usuario = db.relationship("Usuario", back_populates="penalidades")
    emprestimo = db.relationship("Emprestimo", back_populates="penalidade")

    def aplicar(self, usuario, emprestimo) -> None:
        dias_atraso = emprestimo.calcular_dias_atraso()
        self.usuario_id = usuario.id
        self.emprestimo_id = emprestimo.id
        self.valor_multa = self._calcular_multa(dias_atraso)
        self.status = StatusPenalidade.PENDENTE.value
        self._bloquear_usuario(usuario)

    def confirmar_pagamento(self) -> None:
        self.status = StatusPenalidade.PAGA.value
        self.data_pagamento = datetime.utcnow()
        self.desbloquear_usuario()
        db.session.commit()

    def desbloquear_usuario(self) -> None:
        if self.usuario:
            self.usuario.desbloquear()

    @staticmethod
    def listar_por_usuario(usuario_id: str) -> list:
        return Penalidade.query.filter_by(usuario_id=usuario_id).all()

    def _calcular_multa(self, dias_atraso: int) -> float:
        return max(dias_atraso, 1) * MULTA_POR_DIA

    def _bloquear_usuario(self, usuario) -> None:
        usuario.bloquear()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "emprestimo_id": self.emprestimo_id,
            "jogo_nome": self.emprestimo.jogo.nome if self.emprestimo and self.emprestimo.jogo else None,
            "valor_multa": self.valor_multa,
            "status": self.status,
            "data_aplicacao": self.data_aplicacao.isoformat() if self.data_aplicacao else None,
            "data_pagamento": self.data_pagamento.isoformat() if self.data_pagamento else None,
        }