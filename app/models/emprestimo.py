import uuid
from datetime import datetime, date
from enum import Enum
from app.database import db


class StatusEmprestimo(str, Enum):
    ATIVO = "ATIVO"
    DEVOLVIDO = "DEVOLVIDO"
    CANCELADO = "CANCELADO"


class Emprestimo(db.Model):
    __tablename__ = "emprestimos"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dono_id = db.Column(db.String(36), db.ForeignKey("usuarios.id"), nullable=False)
    solicitante_id = db.Column(db.String(36), db.ForeignKey("usuarios.id"), nullable=False)
    jogo_id = db.Column(db.String(36), db.ForeignKey("jogos.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=StatusEmprestimo.ATIVO.value)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_prazo = db.Column(db.DateTime, nullable=False)
    data_devolvido = db.Column(db.DateTime, nullable=True)

    dono = db.relationship("Usuario", back_populates="emprestimos_como_dono", foreign_keys=[dono_id])
    solicitante = db.relationship("Usuario", back_populates="emprestimos_como_solicitante", foreign_keys=[solicitante_id])
    jogo = db.relationship("Jogo", back_populates="emprestimos")
    mensagens = db.relationship("Mensagem", back_populates="emprestimo", lazy=True)
    notificacoes = db.relationship("Notificacao", back_populates="emprestimo", lazy=True)
    penalidade = db.relationship("Penalidade", back_populates="emprestimo", uselist=False)

    def solicitar(self, solicitante, jogo, data_prazo: datetime) -> None:
        if not self._validar_solicitacao(solicitante, jogo):
            raise ValueError("Solicitação inválida.")
        self.solicitante_id = solicitante.id
        self.dono_id = jogo.dono_id
        self.jogo_id = jogo.id
        self.data_prazo = data_prazo
        self.status = StatusEmprestimo.ATIVO.value

    def cancelar(self) -> None:
        from app.models.jogo import StatusJogo
        self.status = StatusEmprestimo.CANCELADO.value
        self.jogo.atualizar_status(StatusJogo.DISPONIVEL.value)

    def confirmar_devolucao(self) -> None:
        from app.models.jogo import StatusJogo
        self.data_devolvido = datetime.utcnow()
        self.status = StatusEmprestimo.DEVOLVIDO.value
        self.jogo.atualizar_status(StatusJogo.DISPONIVEL.value)

    def verificar_atraso(self) -> bool:
        return datetime.utcnow() > self.data_prazo and self.status == StatusEmprestimo.ATIVO.value

    def calcular_dias_atraso(self) -> int:
        if not self.verificar_atraso():
            return 0
        delta = datetime.utcnow() - self.data_prazo
        return delta.days

    def atualizar_status(self, novo_status: str) -> None:
        self.status = novo_status
        db.session.commit()

    def registrar(self) -> None:
        db.session.add(self)
        db.session.commit()

    def _validar_solicitacao(self, solicitante, jogo) -> bool:
        from app.models.usuario import StatusUsuario
        from app.models.jogo import StatusJogo
        if solicitante.status == StatusUsuario.BLOQUEADO.value:
            raise ValueError("Usuário bloqueado não pode solicitar empréstimos.")
        if jogo.status != StatusJogo.DISPONIVEL.value:
            raise ValueError("Jogo não está disponível.")
        if jogo.dono_id == solicitante.id:
            raise ValueError("Você não pode solicitar empréstimo do seu próprio jogo.")
        return True

    def _notificar_partes(self) -> None:
        pass

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "dono_id": self.dono_id,
            "dono_nome": self.dono.nome if self.dono else None,
            "solicitante_id": self.solicitante_id,
            "solicitante_nome": self.solicitante.nome if self.solicitante else None,
            "jogo_id": self.jogo_id,
            "jogo_nome": self.jogo.nome if self.jogo else None,
            "status": self.status,
            "data_inicio": self.data_inicio.isoformat() if self.data_inicio else None,
            "data_prazo": self.data_prazo.isoformat() if self.data_prazo else None,
            "data_devolvido": self.data_devolvido.isoformat() if self.data_devolvido else None,
            "em_atraso": self.verificar_atraso(),
            "dias_atraso": self.calcular_dias_atraso(),
        }
