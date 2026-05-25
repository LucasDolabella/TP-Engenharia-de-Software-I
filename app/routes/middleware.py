from functools import wraps
from flask import request, jsonify
from app.services.auth_service import AuthService


def requer_autenticacao(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"erro": "Token de autenticação necessário."}), 401
        token = auth_header[7:]
        try:
            usuario = AuthService.obter_usuario_por_token(token)
        except ValueError as e:
            return jsonify({"erro": str(e)}), 401
        return f(usuario, *args, **kwargs)
    return decorated