from flask import Blueprint, request, jsonify
from app import db
from app.models.invitation import Invitation
from app.models.guest import Guest
from datetime import datetime

public_bp = Blueprint('public', __name__)

@public_bp.route('/invitations/<code>', methods=['GET'])
def get_public_invitation(code):
    """Obtener invitación por código único (público)"""
    invitation = Invitation.query.filter_by(unique_code=code).first()
    
    if not invitation or not invitation.is_published:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    invitation_data = invitation.to_dict_with_template()
    
    return jsonify({
        'invitation': invitation_data,
        'guests': [g.to_dict() for g in invitation.guests]
    }), 200

@public_bp.route('/invitations/<code>/rsvp', methods=['POST'])
def submit_rsvp(code):
    """Enviar RSVP para una invitación"""
    invitation = Invitation.query.filter_by(unique_code=code).first()
    
    if not invitation or not invitation.is_published:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('guest_name') or data.get('rsvp_status') not in ['accepted', 'declined', 'tentative']:
        return jsonify({'message': 'guest_name y rsvp_status (accepted/declined/tentative) son requeridos'}), 400
    
    try:
        guest = Guest(
            invitation_id=invitation.id,
            name=data['guest_name'],
            email=data.get('guest_email'),
            phone=data.get('guest_phone'),
            rsvp_status=data['rsvp_status'],
            rsvp_date=datetime.utcnow(),
            number_of_guests=data.get('number_of_guests', 1),
            dietary_restrictions=data.get('dietary_restrictions'),
            notes=data.get('notes')
        )
        
        db.session.add(guest)
        db.session.commit()
        
        return jsonify({
            'message': 'RSVP registrado exitosamente',
            'guest': guest.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al registrar RSVP: {str(e)}'}), 500

@public_bp.route('/invitations/<code>/guests', methods=['GET'])
def get_invitation_guests(code):
    """Obtener lista de invitados (solo si está publicada)"""
    invitation = Invitation.query.filter_by(unique_code=code).first()
    
    if not invitation or not invitation.is_published:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    return jsonify({
        'guests': [g.to_dict() for g in invitation.guests],
        'total_rsvp': len(invitation.guests),
        'rsvp_summary': {
            'accepted': sum(1 for g in invitation.guests if g.rsvp_status == 'accepted'),
            'declined': sum(1 for g in invitation.guests if g.rsvp_status == 'declined'),
            'pending': sum(1 for g in invitation.guests if g.rsvp_status == 'pending'),
            'tentative': sum(1 for g in invitation.guests if g.rsvp_status == 'tentative')
        }
    }), 200
