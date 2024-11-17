from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

def create_app(config_class=Config):
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    jwt = JWTManager(app)
    CORS(app)

    # Importar Blueprints
    from app.auth import auth_bp
    from app.resources.usuarios import usuarios_bp
    from app.resources.funcionarios import funcionarios_bp
    from app.resources.clientes import clientes_bp
    from app.resources.produtos import produtos_bp
    from app.resources.vendas import vendas_bp
    from app.resources.despesas import despesas_bp
    from app.resources.plantios import plantios_bp
    from app.resources.relatorios import relatorios_bp

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(funcionarios_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(vendas_bp)
    app.register_blueprint(despesas_bp)
    app.register_blueprint(plantios_bp)
    app.register_blueprint(relatorios_bp)

    return app
