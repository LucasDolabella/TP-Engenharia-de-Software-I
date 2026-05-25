import uuid
from datetime import datetime
from enum import Enum
from app.database import db


class StatusJogo(str, Enum):
    DISPONIVEL = "DISPONIVEL"
    EMPRESTADO = "EMPRESTADO"


class Jogo(db.Model):
    __tablename__ = "jogos"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=StatusJogo.DISPONIVEL.value)
    dono_id = db.Column(db.String(36), db.ForeignKey("usuarios.id"), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    dono = db.relationship("Usuario", back_populates="jogos", foreign_keys=[dono_id])
    emprestimos = db.relationship("Emprestimo", back_populates="jogo", lazy=True)

    def cadastrar(self, nome: str, descricao: str, categoria: str) -> None:
        if not self._validar_dados(nome, descricao, categoria):
            raise ValueError("Dados inválidos para cadastro do jogo.")
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria
        self.status = StatusJogo.DISPONIVEL.value

    def atualizar(self, dados: dict) -> None:
        if "nome" in dados:
            self.nome = dados["nome"]
        if "descricao" in dados:
            self.descricao = dados["descricao"]
        if "categoria" in dados:
            self.categoria = dados["categoria"]

    def remover(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def buscar(termo: str) -> list:
        return Jogo.query.filter(
            (Jogo.nome.ilike(f"%{termo}%")) | (Jogo.categoria.ilike(f"%{termo}%"))
        ).all()

    def verificar_disponibilidade(self) -> bool:
        return self.status == StatusJogo.DISPONIVEL.value

    def atualizar_status(self, novo_status: str) -> None:
        self.status = novo_status
        db.session.commit()

    @staticmethod
    def listar_por_categoria(categoria: str) -> list:
        return Jogo.query.filter_by(categoria=categoria).all()

    def _validar_dados(self, nome: str, descricao: str, categoria: str) -> bool:
        return bool(nome and descricao and categoria)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "status": self.status,
            "dono_id": self.dono_id,
            "dono_nome": self.dono.nome if self.dono else None,
            "data_cadastro": self.data_cadastro.isoformat() if self.data_cadastro else None,
        }