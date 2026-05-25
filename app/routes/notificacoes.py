from flask import Blueprint, jsonify
from app.models.notificacao import Notificacao
from app.database import db
from app.routes.middleware import requer_autenticacao

notificacoes_bp = Blueprint("notificacoes", __name__, url_prefix="/api/notificacoes")


@notificacoes_bp.route("", methods=["GET"])
@requer_autenticacao
def listar(usuario_atual):
    notificacoes = Notificacao.listar_por_usuario(usuario_atual.id)
    return jsonify([n.to_dict() for n in notificacoes]), 200


@notificacoes_bp.route("/<notificacao_id>/lida", methods=["PUT"])
@requer_autenticacao
def marcar_lida(usuario_atual, notificacao_id):
    notif = Notificacao.query.get(notificacao_id)
    if not notif or notif.destinatario_id != usuario_atual.id:
        return jsonify({"erro": "Notificação não encontrada."}), 404
    notif.marcar_como_lida()
    return jsonify({"mensagem": "Notificação marcada como lida."}), 200


@notificacoes_bp.route("/marcar-todas-lidas", methods=["PUT"])
@requer_autenticacao
def marcar_todas_lidas(usuario_atual):
    Notificacao.query.filter_by(destinatario_id=usuario_atual.id, lida=False).update({"lida": True})
    db.session.commit()
    return jsonify({"mensagem": "Todas as notificações marcadas como lidas."}), 200