"""
Rotas relacionadas aos plantios.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils import get_plantios, save_plantio, update_plantio, delete_plantio
from app.schemas import PlantioSchema
from datetime import datetime

plantios_bp = Blueprint('plantios', __name__, url_prefix='/plantios')

@plantios_bp.route('/', methods=['POST'])
@jwt_required()
def criar_plantio():
    """
    Cria um novo plantio.
    """
    data = request.get_json()
    schema = PlantioSchema()
    plantio = schema.load(data)
    plantio['id'] = int(datetime.utcnow().timestamp())
    plantio['data_criacao'] = datetime.utcnow().isoformat()
    plantio['data_modificacao'] = datetime.utcnow().isoformat()

    save_plantio(plantio)

    return schema.dump(plantio), 201

@plantios_bp.route('/', methods=['GET'])
@jwt_required()
def listar_plantios():
    """
    Lista todos os plantios.
    """
    plantios = get_plantios()
    schema = PlantioSchema(many=True)
    return schema.dump(plantios), 200

@plantios_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_plantio(id):
    """
    Obtém um plantio pelo ID.
    """
    plantios = get_plantios()
    plantio = next((p for p in plantios if int(p['id']) == id), None)
    if plantio:
        schema = PlantioSchema()
        return schema.dump(plantio), 200
    else:
        return jsonify({"msg": "Plantio não encontrado"}), 404

@plantios_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_plantio_route(id):
    """
    Atualiza um plantio existente.
    """
    data = request.get_json()
    plantios = get_plantios()
    index = next((i for i, p in enumerate(plantios) if int(p['id']) == id), None)
    if index is not None:
        schema = PlantioSchema()
        plantio = schema.load(data, partial=True)
        plantio_existente = plantios[index]
        plantio_existente.update(plantio)
        plantio_existente['data_modificacao'] = datetime.utcnow().isoformat()
        update_plantio(index, plantio_existente)
        return schema.dump(plantio_existente), 200
    else:
        return jsonify({"msg": "Plantio não encontrado"}), 404

@plantios_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_plantio_route(id):
    """
    Exclui um plantio.
    """
    plantios = get_plantios()
    index = next((i for i, p in enumerate(plantios) if int(p['id']) == id), None)
    if index is not None:
        delete_plantio(index)
        return jsonify({"msg": "Plantio excluído com sucesso"}), 200
    else:
        return jsonify({"msg": "Plantio não encontrado"}), 404
