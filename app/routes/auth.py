from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.routes.middleware import requer_autenticacao

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/cadastrar", methods=["POST"])
def cadastrar():
    dados = request.get_json()
    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()
    senha = dados.get("senha", "")
    if not nome or not email or not senha:
        return jsonify({"erro": "Nome, e-mail e senha são obrigatórios."}), 400
    try:
        resultado = AuthService.cadastrar(nome, email, senha)
        return jsonify(resultado), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 409


@auth_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    email = dados.get("email", "")
    senha = dados.get("senha", "")
    try:
        resultado = AuthService.login(email, senha)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 401


@auth_bp.route("/perfil", methods=["GET"])
@requer_autenticacao
def perfil(usuario_atual):
    return jsonify(usuario_atual.to_dict()), 200


@auth_bp.route("/perfil", methods=["PUT"])
@requer_autenticacao
def atualizar_perfil(usuario_atual):
    from app.database import db
    dados = request.get_json()
    usuario_atual.atualizar_perfil(dados)
    db.session.commit()
    return jsonify(usuario_atual.to_dict()), 200