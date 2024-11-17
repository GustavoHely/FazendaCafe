"""
Rotas relacionadas às vendas.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils import get_vendas, save_venda, update_venda, delete_venda
from app.schemas import VendaSchema
from datetime import datetime

vendas_bp = Blueprint('vendas', __name__, url_prefix='/vendas')

@vendas_bp.route('/', methods=['POST'])
@jwt_required()
def criar_venda():
    """
    Cria uma nova venda.
    """
    data = request.get_json()
    schema = VendaSchema()
    venda = schema.load(data)
    venda['id'] = int(datetime.utcnow().timestamp())
    venda['data_venda'] = datetime.utcnow().isoformat()
    venda['data_criacao'] = datetime.utcnow().isoformat()
    venda['data_modificacao'] = datetime.utcnow().isoformat()

    # Calcular valor total
    venda['valor_total'] = sum([item['quantidade'] * item['preco_unitario'] for item in venda['produtos']])

    save_venda(venda)

    return schema.dump(venda), 201

@vendas_bp.route('/', methods=['GET'])
@jwt_required()
def listar_vendas():
    """
    Lista todas as vendas.
    """
    vendas = get_vendas()
    schema = VendaSchema(many=True)
    return schema.dump(vendas), 200

@vendas_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_venda(id):
    """
    Obtém uma venda pelo ID.
    """
    vendas = get_vendas()
    venda = next((v for v in vendas if int(v['id']) == id), None)
    if venda:
        schema = VendaSchema()
        return schema.dump(venda), 200
    else:
        return jsonify({"msg": "Venda não encontrada"}), 404

@vendas_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_venda_route(id):
    """
    Atualiza uma venda existente.
    """
    data = request.get_json()
    vendas = get_vendas()
    index = next((i for i, v in enumerate(vendas) if int(v['id']) == id), None)
    if index is not None:
        schema = VendaSchema()
        venda = schema.load(data, partial=True)
        venda_existente = vendas[index]
        venda_existente.update(venda)
        venda_existente['data_modificacao'] = datetime.utcnow().isoformat()

        # Recalcular valor total se produtos foram atualizados
        if 'produtos' in venda:
            venda_existente['valor_total'] = sum([item['quantidade'] * item['preco_unitario'] for item in venda_existente['produtos']])

        update_venda(index, venda_existente)
        return schema.dump(venda_existente), 200
    else:
        return jsonify({"msg": "Venda não encontrada"}), 404

@vendas_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_venda_route(id):
    """
    Exclui uma venda.
    """
    vendas = get_vendas()
    index = next((i for i, v in enumerate(vendas) if int(v['id']) == id), None)
    if index is not None:
        delete_venda(index)
        return jsonify({"msg": "Venda excluída com sucesso"}), 200
    else:
        return jsonify({"msg": "Venda não encontrada"}), 404
