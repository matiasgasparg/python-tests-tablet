from flask import Blueprint, request, jsonify
from app import db
from app.models.invitation import Invitation
from app.models.guest import Guest
from datetime import datetime

public_bp = Blueprint('public', __name__)

@public_bp.route('/invitations/<code>', methods=['GET'])
def get_public_invitation(code):
    """
    Obtener invitacion por codigo unico (publico). Devuelve solo invitados confirmados.
    ---
    tags:
      - public
    parameters:
      - in: path
        name: code
        required: true
        type: string
    responses:
      200:
        description: Invitacion publica
      404:
        description: Invitacion no encontrada
    """
    invitation = Invitation.query.filter_by(unique_code=code).first()
    
    if not invitation or not invitation.is_published:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    invitation_data = invitation.to_dict()

    # Importante: por defecto no exponemos el "registro" de invitados públicamente.
    # El cliente (dueño) lo ve vía /api/invitations/<id>/guests con JWT.
    return jsonify({
        'invitation': invitation_data,
        'rsvp_stats': invitation.rsvp_stats(),
    }), 200

@public_bp.route('/invitations/<code>/rsvp', methods=['POST'])
def submit_rsvp(code):
    """
    Enviar RSVP para una invitacion
    ---
    tags:
      - public
    parameters:
      - in: path
        name: code
        required: true
        type: string
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - guest_name
            - rsvp_status
          properties:
            guest_name:
              type: string
              example: Juan Martinez
            guest_email:
              type: string
              example: juan@example.com
            guest_phone:
              type: string
              example: "+34 987 654 321"
            rsvp_status:
              type: string
              example: accepted
            number_of_guests:
              type: integer
              example: 2
            dietary_restrictions:
              type: string
            notes:
              type: string
    responses:
      201:
        description: RSVP registrado
      400:
        description: Datos invalidos
      404:
        description: Invitacion no encontrada
      500:
        description: Error al registrar RSVP
    """
    invitation = Invitation.query.filter_by(unique_code=code).first()
    
    if not invitation or not invitation.is_published:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('guest_name') or data.get('rsvp_status') not in ['accepted', 'declined', 'tentative']:
        return jsonify({'message': 'guest_name y rsvp_status (accepted/declined/tentative) son requeridos'}), 400
    
    try:
        # Upsert simple para evitar duplicados obvios (email/phone)
        existing = None
        if data.get('guest_email'):
            existing = Guest.query.filter_by(invitation_id=invitation.id, email=data['guest_email']).first()
        if not existing and data.get('guest_phone'):
            existing = Guest.query.filter_by(invitation_id=invitation.id, phone=data['guest_phone']).first()

        number_of_guests = data.get('number_of_guests', 1)
        if number_of_guests is None:
            number_of_guests = 1
        if not isinstance(number_of_guests, int) or number_of_guests < 1:
            return jsonify({'message': 'number_of_guests debe ser un entero >= 1'}), 400

        if existing:
            existing.name = data.get('guest_name', existing.name)
            existing.rsvp_status = data['rsvp_status']
            existing.rsvp_date = datetime.utcnow()
            existing.number_of_guests = number_of_guests
            existing.dietary_restrictions = data.get('dietary_restrictions')
            existing.notes = data.get('notes')
            guest = existing
            status_code = 200
        else:
            guest = Guest(
                invitation_id=invitation.id,
                name=data['guest_name'],
                email=data.get('guest_email'),
                phone=data.get('guest_phone'),
                rsvp_status=data['rsvp_status'],
                rsvp_date=datetime.utcnow(),
                number_of_guests=number_of_guests,
                dietary_restrictions=data.get('dietary_restrictions'),
                notes=data.get('notes')
            )
            db.session.add(guest)
            status_code = 201

        db.session.commit()

        return jsonify({
            'message': 'RSVP registrado exitosamente',
            'guest': guest.to_dict(),
            'rsvp_stats': invitation.rsvp_stats(),
        }), status_code
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al registrar RSVP: {str(e)}'}), 500

@public_bp.route('/invitations/<code>/guests', methods=['GET'])
def get_invitation_guests(code):
    """
    Obtener lista de invitados confirmados (solo si esta publicada)
    ---
    tags:
      - public
    parameters:
      - in: path
        name: code
        required: true
        type: string
    responses:
      200:
        description: Lista de invitados
      404:
        description: Invitacion no encontrada
    """
    invitation = Invitation.query.filter_by(unique_code=code).first()
    
    if not invitation or not invitation.is_published:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    confirmed_guests = [g for g in invitation.guests if g.rsvp_status == 'accepted']
    
    return jsonify({
        'guests': [g.to_dict() for g in confirmed_guests],
        'total_confirmed': len(confirmed_guests)
    }), 200
