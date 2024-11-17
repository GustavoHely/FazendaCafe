"""
Rotas relacionadas aos funcionários.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils import get_funcionarios, save_funcionario, update_funcionario, delete_funcionario
from app.schemas import FuncionarioSchema
from datetime import datetime

funcionarios_bp = Blueprint('funcionarios', __name__, url_prefix='/funcionarios')

@funcionarios_bp.route('/', methods=['POST'])
@jwt_required()
def criar_funcionario():
    """
    Cria um novo funcionário.
    """
    data = request.get_json()
    schema = FuncionarioSchema()
    funcionario = schema.load(data)
    funcionario['id'] = int(datetime.utcnow().timestamp())
    funcionario['data_criacao'] = datetime.utcnow().isoformat()
    funcionario['data_modificacao'] = datetime.utcnow().isoformat()

    save_funcionario(funcionario)

    return schema.dump(funcionario), 201

@funcionarios_bp.route('/', methods=['GET'])
@jwt_required()
def listar_funcionarios():
    """
    Lista todos os funcionários.
    """
    funcionarios = get_funcionarios()
    schema = FuncionarioSchema(many=True)
    return schema.dump(funcionarios), 200

@funcionarios_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_funcionario(id):
    """
    Obtém um funcionário pelo ID.
    """
    funcionarios = get_funcionarios()
    funcionario = next((f for f in funcionarios if int(f['id']) == id), None)
    if funcionario:
        schema = FuncionarioSchema()
        return schema.dump(funcionario), 200
    else:
        return jsonify({"msg": "Funcionário não encontrado"}), 404

@funcionarios_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_funcionario_route(id):
    """
    Atualiza um funcionário existente.
    """
    data = request.get_json()
    funcionarios = get_funcionarios()
    index = next((i for i, f in enumerate(funcionarios) if int(f['id']) == id), None)
    if index is not None:
        schema = FuncionarioSchema()
        funcionario = schema.load(data, partial=True)
        funcionario_existente = funcionarios[index]
        funcionario_existente.update(funcionario)
        funcionario_existente['data_modificacao'] = datetime.utcnow().isoformat()
        update_funcionario(index, funcionario_existente)
        return schema.dump(funcionario_existente), 200
    else:
        return jsonify({"msg": "Funcionário não encontrado"}), 404

@funcionarios_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_funcionario_route(id):
    """
    Exclui um funcionário.
    """
    funcionarios = get_funcionarios()
    index = next((i for i, f in enumerate(funcionarios) if int(f['id']) == id), None)
    if index is not None:
        delete_funcionario(index)
        return jsonify({"msg": "Funcionário excluído com sucesso"}), 200
    else:
        return jsonify({"msg": "Funcionário não encontrado"}), 404
