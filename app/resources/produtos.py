"""
Rotas relacionadas aos produtos.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils import get_produtos, save_produto, update_produto, delete_produto
from app.schemas import ProdutoSchema
from datetime import datetime

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@produtos_bp.route('/', methods=['POST'])
@jwt_required()
def criar_produto():
    """
    Cria um novo produto.
    """
    data = request.get_json()
    schema = ProdutoSchema()
    produto = schema.load(data)
    produto['id'] = int(datetime.utcnow().timestamp())
    produto['data_criacao'] = datetime.utcnow().isoformat()
    produto['data_modificacao'] = datetime.utcnow().isoformat()

    save_produto(produto)

    return schema.dump(produto), 201

@produtos_bp.route('/', methods=['GET'])
@jwt_required()
def listar_produtos():
    """
    Lista todos os produtos.
    """
    produtos = get_produtos()
    schema = ProdutoSchema(many=True)
    return schema.dump(produtos), 200

@produtos_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_produto(id):
    """
    Obtém um produto pelo ID.
    """
    produtos = get_produtos()
    produto = next((p for p in produtos if int(p['id']) == id), None)
    if produto:
        schema = ProdutoSchema()
        return schema.dump(produto), 200
    else:
        return jsonify({"msg": "Produto não encontrado"}), 404

@produtos_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_produto_route(id):
    """
    Atualiza um produto existente.
    """
    data = request.get_json()
    produtos = get_produtos()
    index = next((i for i, p in enumerate(produtos) if int(p['id']) == id), None)
    if index is not None:
        schema = ProdutoSchema()
        produto = schema.load(data, partial=True)
        produto_existente = produtos[index]
        produto_existente.update(produto)
        produto_existente['data_modificacao'] = datetime.utcnow().isoformat()
        update_produto(index, produto_existente)
        return schema.dump(produto_existente), 200
    else:
        return jsonify({"msg": "Produto não encontrado"}), 404

@produtos_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_produto_route(id):
    """
    Exclui um produto.
    """
    produtos = get_produtos()
    index = next((i for i, p in enumerate(produtos) if int(p['id']) == id), None)
    if index is not None:
        delete_produto(index)
        return jsonify({"msg": "Produto excluído com sucesso"}), 200
    else:
        return jsonify({"msg": "Produto não encontrado"}), 404
