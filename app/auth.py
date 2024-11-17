"""
Módulo de autenticação e autorização.
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.utils import get_usuarios, save_usuario
from app.schemas import UsuarioSchema
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Rota para autenticação de usuários.
    """
    email = request.json.get('email')
    senha = request.json.get('senha')

    usuarios = get_usuarios()
    usuario = next((u for u in usuarios if u['email'] == email), None)

    if usuario and check_password_hash(usuario['senha_hash'], senha):
        access_token = create_access_token(identity=usuario['id'], expires_delta=timedelta(hours=1))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Credenciais inválidas"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Rota para registro de novos usuários.
    """
    data = request.get_json()
    schema = UsuarioSchema()
    usuario = schema.load(data)
    usuario['id'] = int(datetime.utcnow().timestamp())
    usuario['data_criacao'] = datetime.utcnow().isoformat()
    usuario['data_modificacao'] = datetime.utcnow().isoformat()

    usuario['senha_hash'] = generate_password_hash(usuario.pop('senha'))
    save_usuario(usuario)

    return schema.dump(usuario), 201
