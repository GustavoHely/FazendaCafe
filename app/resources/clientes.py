"""
Rotas relacionadas aos clientes.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils import get_clientes, save_cliente, update_cliente, delete_cliente
from app.schemas import ClienteSchema
from datetime import datetime

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes_bp.route('/', methods=['POST'])
@jwt_required()
def criar_cliente():
    """
    Cria um novo cliente.
    """
    data = request.get_json()
    schema = ClienteSchema()
    cliente = schema.load(data)
    cliente['id'] = int(datetime.utcnow().timestamp())
    cliente['data_criacao'] = datetime.utcnow().isoformat()
    cliente['data_modificacao'] = datetime.utcnow().isoformat()

    save_cliente(cliente)

    return schema.dump(cliente), 201

@clientes_bp.route('/', methods=['GET'])
@jwt_required()
def listar_clientes():
    """
    Lista todos os clientes.
    """
    clientes = get_clientes()
    schema = ClienteSchema(many=True)
    return schema.dump(clientes), 200

@clientes_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_cliente(id):
    """
    Obtém um cliente pelo ID.
    """
    clientes = get_clientes()
    cliente = next((c for c in clientes if int(c['id']) == id), None)
    if cliente:
        schema = ClienteSchema()
        return schema.dump(cliente), 200
    else:
        return jsonify({"msg": "Cliente não encontrado"}), 404

@clientes_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_cliente_route(id):
    """
    Atualiza um cliente existente.
    """
    data = request.get_json()
    clientes = get_clientes()
    index = next((i for i, c in enumerate(clientes) if int(c['id']) == id), None)
    if index is not None:
        schema = ClienteSchema()
        cliente = schema.load(data, partial=True)
        cliente_existente = clientes[index]
        cliente_existente.update(cliente)
        cliente_existente['data_modificacao'] = datetime.utcnow().isoformat()
        update_cliente(index, cliente_existente)
        return schema.dump(cliente_existente), 200
    else:
        return jsonify({"msg": "Cliente não encontrado"}), 404

@clientes_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_cliente_route(id):
    """
    Exclui um cliente.
    """
    clientes = get_clientes()
    index = next((i for i, c in enumerate(clientes) if int(c['id']) == id), None)
    if index is not None:
        delete_cliente(index)
        return jsonify({"msg": "Cliente excluído com sucesso"}), 200
    else:
        return jsonify({"msg": "Cliente não encontrado"}), 404
