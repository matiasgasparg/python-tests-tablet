from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

db = SQLAlchemy()
jwt = JWTManager()


def _bootstrap_admin_user(app):
    """Crea un usuario admin si no existe (desde variables de entorno).

    Variables:
      - ADMIN_USERNAME (se guarda en User.email)
      - ADMIN_PASSWORD
      - ADMIN_COMPANY_NAME (opcional)
    """
    from app.models.user import User

    admin_username = os.environ.get('ADMIN_USERNAME')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    admin_company = os.environ.get('ADMIN_COMPANY_NAME', 'Admin')

    if not admin_username or not admin_password:
        return

    with app.app_context():
        existing = User.query.filter_by(email=admin_username).first()
        if existing:
            return

        user = User(email=admin_username, company_name=admin_company)
        user.set_password(admin_password)
        db.session.add(user)
        db.session.commit()


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
    
    # Crear tablas + bootstrap admin
    with app.app_context():
        db.create_all()

    _bootstrap_admin_user(app)

    return app
