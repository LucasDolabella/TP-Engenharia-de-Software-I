from flask import Blueprint, request, jsonify
from app.services.penalidade_service import PenalidadeService
from app.routes.middleware import requer_autenticacao

penalidades_bp = Blueprint("penalidades", __name__, url_prefix="/api/penalidades")


@penalidades_bp.route("", methods=["GET"])
@requer_autenticacao
def listar(usuario_atual):
    penalidades = PenalidadeService.listar_por_usuario(usuario_atual.id)
    return jsonify([p.to_dict() for p in penalidades]), 200


@penalidades_bp.route("/<penalidade_id>/pagar", methods=["POST"])
@requer_autenticacao
def pagar(usuario_atual, penalidade_id):
    dados = request.get_json()
    metodo = dados.get("metodo", "cartao")
    try:
        resultado = PenalidadeService.processar_pagamento(penalidade_id, usuario_atual.id, metodo)
        status_code = 200 if resultado["sucesso"] else 402
        return jsonify(resultado), status_code
    except (ValueError, PermissionError) as e:
        return jsonify({"erro": str(e)}), 400