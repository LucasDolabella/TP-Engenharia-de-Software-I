from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from app.routes.middleware import requer_autenticacao

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")


@chat_bp.route("/<emprestimo_id>", methods=["GET"])
@requer_autenticacao
def listar_mensagens(usuario_atual, emprestimo_id):
    try:
        ChatService.marcar_como_lidas(emprestimo_id, usuario_atual.id)
        mensagens = ChatService.listar_mensagens(emprestimo_id, usuario_atual.id)
        return jsonify([m.to_dict() for m in mensagens]), 200
    except (ValueError, PermissionError) as e:
        return jsonify({"erro": str(e)}), 400


@chat_bp.route("/<emprestimo_id>", methods=["POST"])
@requer_autenticacao
def enviar_mensagem(usuario_atual, emprestimo_id):
    dados = request.get_json()
    conteudo = dados.get("conteudo", "").strip()
    if not conteudo:
        return jsonify({"erro": "Mensagem não pode ser vazia."}), 400
    try:
        mensagem = ChatService.enviar_mensagem(emprestimo_id, usuario_atual, conteudo)
        return jsonify(mensagem.to_dict()), 201
    except (ValueError, PermissionError) as e:
        return jsonify({"erro": str(e)}), 400