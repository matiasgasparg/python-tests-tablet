from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='development'):
    """Factory pattern para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    from config import config
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.invitations import invitations_bp
    from app.routes.admin import admin_bp
    from app.routes.public import public_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(invitations_bp, url_prefix='/api/invitations')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(public_bp, url_prefix='/api/public')
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    return app
