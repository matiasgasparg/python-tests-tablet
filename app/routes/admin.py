from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.template import Template
from app.models.user import User
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/templates', methods=['POST'])
@jwt_required()
def create_template():
    """Crear nuevo template de invitación"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'message': 'El nombre del template es requerido'}), 400
    
    template = Template(
        user_id=user_id,
        name=data['name'],
        description=data.get('description'),
        title=data.get('title', '¡Te invitamos a celebrar!'),
        subtitle=data.get('subtitle', 'Un día especial'),
        header_text=data.get('header_text', ''),
        footer_text=data.get('footer_text', ''),
        primary_color=data.get('primary_color', '#FF69B4'),
        secondary_color=data.get('secondary_color', '#FFD700'),
        text_color=data.get('text_color', '#333333'),
        background_color=data.get('background_color', '#FFFFFF'),
        logo_url=data.get('logo_url'),
        background_image_url=data.get('background_image_url'),
        is_default=data.get('is_default', False)
    )
    
    db.session.add(template)
    db.session.commit()
    
    return jsonify({
        'message': 'Template creado exitosamente',
        'template': template.to_dict()
    }), 201

@admin_bp.route('/templates', methods=['GET'])
@jwt_required()
def list_templates():
    """Listar templates del usuario actual"""
    user_id = get_jwt_identity()
    
    templates = Template.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'templates': [t.to_dict() for t in templates],
        'total': len(templates)
    }), 200

@admin_bp.route('/templates/<int:template_id>', methods=['GET'])
@jwt_required()
def get_template(template_id):
    """Obtener detalles de un template"""
    user_id = get_jwt_identity()
    template = Template.query.get(template_id)
    
    if not template or template.user_id != user_id:
        return jsonify({'message': 'Template no encontrado'}), 404
    
    return jsonify(template.to_dict()), 200

@admin_bp.route('/templates/<int:template_id>', methods=['PUT'])
@jwt_required()
def update_template(template_id):
    """Actualizar template"""
    user_id = get_jwt_identity()
    template = Template.query.get(template_id)
    
    if not template or template.user_id != user_id:
        return jsonify({'message': 'Template no encontrado'}), 404
    
    data = request.get_json()
    
    # Campos actualizables
    updateable_fields = [
        'name', 'description', 'title', 'subtitle', 'header_text', 'footer_text',
        'primary_color', 'secondary_color', 'text_color', 'background_color',
        'logo_url', 'background_image_url', 'is_active', 'is_default'
    ]
    
    for field in updateable_fields:
        if field in data:
            setattr(template, field, data[field])
    
    template.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Template actualizado exitosamente',
        'template': template.to_dict()
    }), 200

@admin_bp.route('/templates/<int:template_id>', methods=['DELETE'])
@jwt_required()
def delete_template(template_id):
    """Eliminar template"""
    user_id = get_jwt_identity()
    template = Template.query.get(template_id)
    
    if not template or template.user_id != user_id:
        return jsonify({'message': 'Template no encontrado'}), 404
    
    # No permitir eliminar templates que estén en uso
    if template.invitations:
        return jsonify({'message': 'No puedes eliminar un template que está en uso'}), 409
    
    db.session.delete(template)
    db.session.commit()
    
    return jsonify({'message': 'Template eliminado exitosamente'}), 200

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Obtener estadísticas del usuario"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    from app.models.invitation import Invitation
    from app.models.guest import Guest
    
    total_invitations = Invitation.query.filter_by(user_id=user_id).count()
    total_guests = db.session.query(Guest).join(Invitation).filter(Invitation.user_id == user_id).count()
    published_invitations = Invitation.query.filter_by(user_id=user_id, is_published=True).count()
    
    # RSVP stats
    rsvp_accepted = db.session.query(Guest).join(Invitation).filter(
        Invitation.user_id == user_id,
        Guest.rsvp_status == 'accepted'
    ).count()
    
    rsvp_declined = db.session.query(Guest).join(Invitation).filter(
        Invitation.user_id == user_id,
        Guest.rsvp_status == 'declined'
    ).count()
    
    rsvp_pending = db.session.query(Guest).join(Invitation).filter(
        Invitation.user_id == user_id,
        Guest.rsvp_status == 'pending'
    ).count()
    
    return jsonify({
        'total_invitations': total_invitations,
        'published_invitations': published_invitations,
        'total_templates': len(user.templates),
        'total_guests': total_guests,
        'rsvp_accepted': rsvp_accepted,
        'rsvp_declined': rsvp_declined,
        'rsvp_pending': rsvp_pending
    }), 200
