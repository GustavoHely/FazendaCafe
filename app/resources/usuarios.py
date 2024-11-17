"""
Rotas relacionadas aos usuários.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils import get_usuarios, save_usuario, update_usuario, delete_usuario
from app.schemas import UsuarioSchema
from datetime import datetime
from werkzeug.security import generate_password_hash

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuarios_bp.route('/', methods=['GET'])
@jwt_required()
def listar_usuarios():
    """
    Lista todos os usuários.
    """
    usuarios = get_usuarios()
    schema = UsuarioSchema(many=True)
    return schema.dump(usuarios), 200

@usuarios_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_usuario(id):
    """
    Obtém um usuário pelo ID.
    """
    usuarios = get_usuarios()
    usuario = next((u for u in usuarios if int(u['id']) == id), None)
    if usuario:
        schema = UsuarioSchema()
        return schema.dump(usuario), 200
    else:
        return jsonify({"msg": "Usuário não encontrado"}), 404

@usuarios_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_usuario_route(id):
    """
    Atualiza um usuário existente.
    """
    data = request.get_json()
    usuarios = get_usuarios()
    usuario_atualizado = update_usuario(id, data)
    if usuario_atualizado:
        schema = UsuarioSchema()
        # Como update_row retorna a resposta da API do Google Sheets, precisamos buscar novamente o usuário atualizado
        usuarios = get_usuarios()
        usuario = next((u for u in usuarios if int(u['id']) == id), None)
        return schema.dump(usuario), 200
    else:
        return jsonify({"msg": "Usuário não encontrado"}), 404

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_usuario_route(id):
    """
    Exclui um usuário.
    """
    result = delete_usuario(id)
    if result:
        return jsonify({"msg": "Usuário excluído com sucesso"}), 200
    else:
        return jsonify({"msg": "Usuário não encontrado"}), 404
