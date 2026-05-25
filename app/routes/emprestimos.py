from flask import Blueprint, request, jsonify
from app.services.emprestimo_service import EmprestimoService
from app.services.jogo_service import JogoService
from app.routes.middleware import requer_autenticacao

emprestimos_bp = Blueprint("emprestimos", __name__, url_prefix="/api/emprestimos")


@emprestimos_bp.route("", methods=["GET"])
@requer_autenticacao
def listar(usuario_atual):
    emprestimos = EmprestimoService.listar_por_usuario(usuario_atual.id)
    return jsonify([e.to_dict() for e in emprestimos]), 200


@emprestimos_bp.route("/<emprestimo_id>", methods=["GET"])
@requer_autenticacao
def obter(usuario_atual, emprestimo_id):
    try:
        emprestimo = EmprestimoService.obter(emprestimo_id)
        if usuario_atual.id not in (emprestimo.dono_id, emprestimo.solicitante_id):
            return jsonify({"erro": "Acesso não autorizado."}), 403
        return jsonify(emprestimo.to_dict()), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@emprestimos_bp.route("", methods=["POST"])
@requer_autenticacao
def solicitar(usuario_atual):
    dados = request.get_json()
    jogo_id = dados.get("jogo_id")
    data_prazo = dados.get("data_prazo")
    if not jogo_id or not data_prazo:
        return jsonify({"erro": "jogo_id e data_prazo são obrigatórios."}), 400
    try:
        jogo = JogoService.obter(jogo_id)
        emprestimo = EmprestimoService.solicitar(usuario_atual, jogo, data_prazo)
        return jsonify(emprestimo.to_dict()), 201
    except (ValueError, PermissionError) as e:
        return jsonify({"erro": str(e)}), 400


@emprestimos_bp.route("/<emprestimo_id>/confirmar-devolucao", methods=["PUT"])
@requer_autenticacao
def confirmar_devolucao(usuario_atual, emprestimo_id):
    try:
        emprestimo = EmprestimoService.confirmar_devolucao(emprestimo_id, usuario_atual.id)
        return jsonify(emprestimo.to_dict()), 200
    except (ValueError, PermissionError) as e:
        return jsonify({"erro": str(e)}), 400


@emprestimos_bp.route("/<emprestimo_id>/nao-devolvido", methods=["PUT"])
@requer_autenticacao
def nao_devolvido(usuario_atual, emprestimo_id):
    try:
        emprestimo = EmprestimoService.registrar_nao_devolucao(emprestimo_id, usuario_atual.id)
        return jsonify(emprestimo.to_dict()), 200
    except (ValueError, PermissionError) as e:
        return jsonify({"erro": str(e)}), 400


@emprestimos_bp.route("/<emprestimo_id>/cancelar", methods=["PUT"])
@requer_autenticacao
def cancelar(usuario_atual, emprestimo_id):
    try:
        emprestimo = EmprestimoService.cancelar(emprestimo_id, usuario_atual.id)
        return jsonify(emprestimo.to_dict()), 200
    except (ValueError, PermissionError) as e:
        return jsonify({"erro": str(e)}), 400