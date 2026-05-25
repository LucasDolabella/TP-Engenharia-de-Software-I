from flask import Blueprint, request, jsonify
from app.services.jogo_service import JogoService
from app.routes.middleware import requer_autenticacao

jogos_bp = Blueprint("jogos", __name__, url_prefix="/api/jogos")


@jogos_bp.route("", methods=["GET"])
def listar():
    busca = request.args.get("busca", "")
    jogos = JogoService.listar_todos(busca if busca else None)
    return jsonify([j.to_dict() for j in jogos]), 200


@jogos_bp.route("/meus", methods=["GET"])
@requer_autenticacao
def meus_jogos(usuario_atual):
    jogos = JogoService.listar_por_usuario(usuario_atual.id)
    return jsonify([j.to_dict() for j in jogos]), 200


@jogos_bp.route("/<jogo_id>", methods=["GET"])
def obter(jogo_id):
    try:
        jogo = JogoService.obter(jogo_id)
        return jsonify(jogo.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@jogos_bp.route("", methods=["POST"])
@requer_autenticacao
def cadastrar(usuario_atual):
    dados = request.get_json()
    nome = dados.get("nome", "").strip()
    descricao = dados.get("descricao", "").strip()
    categoria = dados.get("categoria", "").strip()
    if not nome or not descricao or not categoria:
        return jsonify({"erro": "Nome, descrição e categoria são obrigatórios."}), 400
    try:
        jogo = JogoService.cadastrar(nome, descricao, categoria, usuario_atual.id)
        return jsonify(jogo.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@jogos_bp.route("/<jogo_id>", methods=["PUT"])
@requer_autenticacao
def atualizar(usuario_atual, jogo_id):
    dados = request.get_json()
    try:
        jogo = JogoService.atualizar(jogo_id, usuario_atual.id, dados)
        return jsonify(jogo.to_dict()), 200
    except (ValueError, PermissionError) as e:
        return jsonify({"erro": str(e)}), 400


@jogos_bp.route("/<jogo_id>", methods=["DELETE"])
@requer_autenticacao
def remover(usuario_atual, jogo_id):
    try:
        JogoService.remover(jogo_id, usuario_atual.id)
        return jsonify({"mensagem": "Jogo removido com sucesso."}), 200
    except (ValueError, PermissionError) as e:
        return jsonify({"erro": str(e)}), 400