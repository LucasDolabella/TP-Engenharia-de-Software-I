import uuid
from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db


class StatusUsuario(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    BLOQUEADO = "BLOQUEADO"


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=StatusUsuario.ATIVO.value)
    avaliacao = db.Column(db.Float, default=0.0)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    jogos = db.relationship("Jogo", back_populates="dono", lazy=True, foreign_keys="Jogo.dono_id")
    emprestimos_como_solicitante = db.relationship(
        "Emprestimo", back_populates="solicitante", lazy=True, foreign_keys="Emprestimo.solicitante_id"
    )
    emprestimos_como_dono = db.relationship(
        "Emprestimo", back_populates="dono", lazy=True, foreign_keys="Emprestimo.dono_id"
    )
    penalidades = db.relationship("Penalidade", back_populates="usuario", lazy=True)
    notificacoes = db.relationship("Notificacao", back_populates="destinatario", lazy=True)

    def cadastrar(self, nome: str, email: str, senha: str) -> None:
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)
        self.status = StatusUsuario.ATIVO.value

    def login(self, email: str, senha: str) -> bool:
        return self.email == email and self._validar_senha(senha)

    def logout(self) -> None:
        pass

    def atualizar_perfil(self, dados: dict) -> None:
        if "nome" in dados:
            self.nome = dados["nome"]
        if "senha" in dados:
            self.senha = generate_password_hash(dados["senha"])

    def avaliar_usuario(self, usuario: "Usuario", nota: float) -> None:
        usuario.avaliacao = nota
        db.session.commit()

    def bloquear(self) -> None:
        self.status = StatusUsuario.BLOQUEADO.value
        db.session.commit()

    def desbloquear(self) -> None:
        self.status = StatusUsuario.ATIVO.value
        db.session.commit()

    def esta_bloqueado(self) -> bool:
        return self.status == StatusUsuario.BLOQUEADO.value

    def _validar_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha, senha)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "status": self.status,
            "avaliacao": self.avaliacao,
            "data_cadastro": self.data_cadastro.isoformat() if self.data_cadastro else None,
        }
