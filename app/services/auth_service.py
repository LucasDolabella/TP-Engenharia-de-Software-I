import jwt
import os
from datetime import datetime, timedelta
from app.database import db
from app.models.usuario import Usuario, StatusUsuario


SECRET_KEY = os.environ.get("SECRET_KEY", "joga-ai-secret-dev-key-2024")


class AuthService:

    @staticmethod
    def cadastrar(nome: str, email: str, senha: str) -> dict:
        if Usuario.query.filter_by(email=email).first():
            raise ValueError("E-mail já cadastrado.")
        usuario = Usuario()
        usuario.cadastrar(nome, email, senha)
        db.session.add(usuario)
        db.session.commit()
        token = AuthService._gerar_token(usuario.id)
        return {"usuario": usuario.to_dict(), "token": token}

    @staticmethod
    def login(email: str, senha: str) -> dict:
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario or not usuario._validar_senha(senha):
            raise ValueError("E-mail ou senha inválidos.")
        token = AuthService._gerar_token(usuario.id)
        return {"usuario": usuario.to_dict(), "token": token}

    @staticmethod
    def obter_usuario_por_token(token: str) -> Usuario:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            usuario = Usuario.query.get(payload["sub"])
            if not usuario:
                raise ValueError("Usuário não encontrado.")
            return usuario
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado.")
        except jwt.InvalidTokenError:
            raise ValueError("Token inválido.")

    @staticmethod
    def _gerar_token(usuario_id: str) -> str:
        payload = {
            "sub": usuario_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=24),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")