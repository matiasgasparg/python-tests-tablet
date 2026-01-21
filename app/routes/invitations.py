from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.invitation import Invitation
from app.models.template import Template
from app.models.user import User
from datetime import datetime

invitations_bp = Blueprint('invitations', __name__)

@invitations_bp.route('', methods=['POST'])
@jwt_required()
def create_invitation():
    """Crear nueva invitación"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    data = request.get_json()
    
    # Validar datos requeridos
    required_fields = ['birthday_name', 'birthday_date', 'event_title', 'event_date']
    if not all(field in data for field in required_fields):
        return jsonify({'message': f'Campos requeridos: {", ".join(required_fields)}'}), 400
    
    try:
        invitation = Invitation(
            user_id=user_id,
            template_id=data.get('template_id'),
            birthday_name=data['birthday_name'],
            birthday_date=datetime.fromisoformat(data['birthday_date']),
            birthday_age=data.get('birthday_age'),
            event_title=data['event_title'],
            event_date=datetime.fromisoformat(data['event_date']),
            event_time=data.get('event_time'),
            event_location=data.get('event_location'),
            event_address=data.get('event_address'),
            organizer_name=data.get('organizer_name'),
            organizer_phone=data.get('organizer_phone'),
            organizer_email=data.get('organizer_email'),
            dress_code=data.get('dress_code'),
            special_notes=data.get('special_notes'),
            rsvp_deadline=datetime.fromisoformat(data['rsvp_deadline']) if data.get('rsvp_deadline') else None
        )
        
        # Generar URL compartible
        invitation.share_url = f"/invitations/{invitation.unique_code}"
        
        db.session.add(invitation)
        db.session.commit()
        
        return jsonify({
            'message': 'Invitación creada exitosamente',
            'invitation': invitation.to_dict_with_template()
        }), 201
    
    except ValueError as e:
        return jsonify({'message': f'Formato de fecha inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear invitación: {str(e)}'}), 500

@invitations_bp.route('', methods=['GET'])
@jwt_required()
def list_invitations():
    """Listar invitaciones del usuario actual"""
    user_id = get_jwt_identity()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    invitations = Invitation.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'invitations': [inv.to_dict_with_template() for inv in invitations.items],
        'total': invitations.total,
        'pages': invitations.pages,
        'current_page': page
    }), 200

@invitations_bp.route('/<int:invitation_id>', methods=['GET'])
@jwt_required()
def get_invitation(invitation_id):
    """Obtener detalles de una invitación"""
    user_id = get_jwt_identity()
    invitation = Invitation.query.get(invitation_id)
    
    if not invitation or invitation.user_id != user_id:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    return jsonify(invitation.to_dict_with_template()), 200

@invitations_bp.route('/<int:invitation_id>', methods=['PUT'])
@jwt_required()
def update_invitation(invitation_id):
    """Actualizar invitación"""
    user_id = get_jwt_identity()
    invitation = Invitation.query.get(invitation_id)
    
    if not invitation or invitation.user_id != user_id:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    data = request.get_json()
    
    try:
        # Actualizar campos
        updateable_fields = [
            'birthday_name', 'birthday_age', 'event_title', 'event_time',
            'event_location', 'event_address', 'organizer_name', 'organizer_phone',
            'organizer_email', 'dress_code', 'special_notes', 'template_id'
        ]
        
        for field in updateable_fields:
            if field in data:
                setattr(invitation, field, data[field])
        
        # Campos con conversión de fecha
        if 'birthday_date' in data:
            invitation.birthday_date = datetime.fromisoformat(data['birthday_date'])
        if 'event_date' in data:
            invitation.event_date = datetime.fromisoformat(data['event_date'])
        if 'rsvp_deadline' in data:
            invitation.rsvp_deadline = datetime.fromisoformat(data['rsvp_deadline']) if data['rsvp_deadline'] else None
        
        invitation.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Invitación actualizada exitosamente',
            'invitation': invitation.to_dict_with_template()
        }), 200
    
    except ValueError as e:
        return jsonify({'message': f'Formato de fecha inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar invitación: {str(e)}'}), 500

@invitations_bp.route('/<int:invitation_id>', methods=['DELETE'])
@jwt_required()
def delete_invitation(invitation_id):
    """Eliminar invitación"""
    user_id = get_jwt_identity()
    invitation = Invitation.query.get(invitation_id)
    
    if not invitation or invitation.user_id != user_id:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    db.session.delete(invitation)
    db.session.commit()
    
    return jsonify({'message': 'Invitación eliminada exitosamente'}), 200

@invitations_bp.route('/<int:invitation_id>/publish', methods=['POST'])
@jwt_required()
def publish_invitation(invitation_id):
    """Publicar invitación"""
    user_id = get_jwt_identity()
    invitation = Invitation.query.get(invitation_id)
    
    if not invitation or invitation.user_id != user_id:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    invitation.is_published = True
    invitation.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Invitación publicada exitosamente',
        'invitation': invitation.to_dict_with_template(),
        'share_url': invitation.share_url
    }), 200
