from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registrar nuevo usuario (administrador).

    Por defecto está deshabilitado para este proyecto (solo admin). Para habilitar:
    setear ALLOW_REGISTER=true en el entorno.
    """
    import os
    if os.environ.get('ALLOW_REGISTER', 'false').lower() not in ['1', 'true', 'yes']:
        return jsonify({'message': 'Registro deshabilitado'}), 403

    data = request.get_json()
    
    # Validar datos requeridos
    if not data or not data.get('email') or not data.get('password') or not data.get('company_name'):
        return jsonify({'message': 'Email, password y company_name son requeridos'}), 400
    
    # Verificar si el usuario ya existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'El email ya está registrado'}), 409
    
    # Crear nuevo usuario
    user = User(
        email=data['email'],
        company_name=data['company_name'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión.

    Acepta `email` o `username`.
    """
    data = request.get_json()

    identifier = None
    if data:
        identifier = data.get('email') or data.get('username')

    if not data or not identifier or not data.get('password'):
        return jsonify({'message': 'email/username y password son requeridos'}), 400

    user = User.query.filter_by(email=identifier).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Email o contraseña incorrectos'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'Usuario inactivo'}), 403
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Inicio de sesión exitoso',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Obtener información del usuario actual"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    return jsonify(user.to_dict()), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Cambiar contraseña del usuario actual"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('old_password') or not data.get('new_password'):
        return jsonify({'message': 'old_password y new_password son requeridos'}), 400
    
    if not user.check_password(data['old_password']):
        return jsonify({'message': 'Contraseña actual incorrecta'}), 401
    
    user.set_password(data['new_password'])
    db.session.commit()
    
    return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200

@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Actualizar perfil del usuario"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    data = request.get_json()
    
    if 'company_name' in data:
        user.company_name = data['company_name']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Perfil actualizado exitosamente',
        'user': user.to_dict()
    }), 200
