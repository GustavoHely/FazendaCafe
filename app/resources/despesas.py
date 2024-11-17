"""
Rotas relacionadas às despesas.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils import get_despesas, save_despesa, update_despesa, delete_despesa
from app.schemas import DespesaSchema
from datetime import datetime

despesas_bp = Blueprint('despesas', __name__, url_prefix='/despesas')

@despesas_bp.route('/', methods=['POST'])
@jwt_required()
def criar_despesa():
    """
    Cria uma nova despesa.
    """
    data = request.get_json()
    schema = DespesaSchema()
    despesa = schema.load(data)
    despesa['id'] = int(datetime.utcnow().timestamp())
    despesa['data_criacao'] = datetime.utcnow().isoformat()
    despesa['data_modificacao'] = datetime.utcnow().isoformat()

    save_despesa(despesa)

    return schema.dump(despesa), 201

@despesas_bp.route('/', methods=['GET'])
@jwt_required()
def listar_despesas():
    """
    Lista todas as despesas.
    """
    despesas = get_despesas()
    schema = DespesaSchema(many=True)
    return schema.dump(despesas), 200

@despesas_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_despesa(id):
    """
    Obtém uma despesa pelo ID.
    """
    despesas = get_despesas()
    despesa = next((d for d in despesas if int(d['id']) == id), None)
    if despesa:
        schema = DespesaSchema()
        return schema.dump(despesa), 200
    else:
        return jsonify({"msg": "Despesa não encontrada"}), 404

@despesas_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_despesa_route(id):
    """
    Atualiza uma despesa existente.
    """
    data = request.get_json()
    despesas = get_despesas()
    index = next((i for i, d in enumerate(despesas) if int(d['id']) == id), None)
    if index is not None:
        schema = DespesaSchema()
        despesa = schema.load(data, partial=True)
        despesa_existente = despesas[index]
        despesa_existente.update(despesa)
        despesa_existente['data_modificacao'] = datetime.utcnow().isoformat()
        update_despesa(index, despesa_existente)
        return schema.dump(despesa_existente), 200
    else:
        return jsonify({"msg": "Despesa não encontrada"}), 404

@despesas_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_despesa_route(id):
    """
    Exclui uma despesa.
    """
    despesas = get_despesas()
    index = next((i for i, d in enumerate(despesas) if int(d['id']) == id), None)
    if index is not None:
        delete_despesa(index)
        return jsonify({"msg": "Despesa excluída com sucesso"}), 200
    else:
        return jsonify({"msg": "Despesa não encontrada"}), 404
