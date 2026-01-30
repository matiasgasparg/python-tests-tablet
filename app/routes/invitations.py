from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.invitation import Invitation
from app.models.user import User
from datetime import datetime

invitations_bp = Blueprint('invitations', __name__)


def _build_public_share_url(invitation: Invitation) -> str:
    """Devuelve URL pública para compartir (absoluta si hay request context)."""
    try:
        # request.host_url incluye el trailing slash
        base = request.host_url.rstrip('/')
        return f"{base}/api/public/invitations/{invitation.unique_code}"
    except Exception:
        # Fallback: relativa
        return f"/api/public/invitations/{invitation.unique_code}"

@invitations_bp.route('', methods=['POST'])
@jwt_required()
def create_invitation():
    """
    Crear nueva invitacion
    ---
    tags:
      - invitations
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - birthday_name
            - birthday_date
            - event_title
            - event_date
          properties:
            birthday_name:
              type: string
              example: Maria Garcia
            birthday_date:
              type: string
              example: "2005-03-15T00:00:00"
            birthday_age:
              type: integer
              example: 18
            event_title:
              type: string
              example: Cumpleanos de Maria
            event_date:
              type: string
              example: "2024-03-16T19:00:00"
            event_time:
              type: string
              example: "19:00"
            event_location:
              type: string
            event_address:
              type: string
            organizer_name:
              type: string
            organizer_phone:
              type: string
            organizer_email:
              type: string
            dress_code:
              type: string
            special_notes:
              type: string
            rsvp_deadline:
              type: string
              example: "2024-03-12T23:59:59"
    responses:
      201:
        description: Invitacion creada
      400:
        description: Datos invalidos
      404:
        description: Usuario no encontrado
      500:
        description: Error al crear invitacion
    """
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
            rsvp_deadline=datetime.fromisoformat(data['rsvp_deadline']) if data.get('rsvp_deadline') else None,
            template_key=data.get('template_key', 'classic_01'),
            hero_image_url=data.get('hero_image_url'),
            image_1_url=data.get('image_1_url'),
            image_2_url=data.get('image_2_url'),
            video_url=data.get('video_url'),
        )
        
        # Generar URL compartible (pública)
        invitation.share_url = _build_public_share_url(invitation)
        
        db.session.add(invitation)
        db.session.commit()
        
        return jsonify({
            'message': 'Invitación creada exitosamente',
            'invitation': invitation.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'message': f'Formato de fecha inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear invitación: {str(e)}'}), 500

@invitations_bp.route('/quick-create', methods=['POST'])
@jwt_required()
def quick_create_and_publish_invitation():
    """Crear + publicar invitación en un solo paso (admin).

    Devuelve un link listo para mandar por WhatsApp.
    ---
    tags:
      - invitations
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - birthday_name
            - birthday_date
            - event_title
            - event_date
          properties:
            birthday_name:
              type: string
            birthday_date:
              type: string
              example: "2005-03-15T00:00:00"
            birthday_age:
              type: integer
            event_title:
              type: string
            event_date:
              type: string
              example: "2026-02-10T19:00:00"
            event_time:
              type: string
            event_location:
              type: string
            event_address:
              type: string
            organizer_name:
              type: string
            organizer_phone:
              type: string
            organizer_email:
              type: string
            dress_code:
              type: string
            special_notes:
              type: string
            rsvp_deadline:
              type: string
            template_key:
              type: string
              example: classic_01
            hero_image_url:
              type: string
            image_1_url:
              type: string
            image_2_url:
              type: string
            video_url:
              type: string
    responses:
      201:
        description: Invitacion creada y publicada
      400:
        description: Datos invalidos
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    data = request.get_json() or {}

    required_fields = ['birthday_name', 'birthday_date', 'event_title', 'event_date']
    if not all(field in data for field in required_fields):
        return jsonify({'message': f'Campos requeridos: {", ".join(required_fields)}'}), 400

    try:
        invitation = Invitation(
            user_id=user_id,
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
            rsvp_deadline=datetime.fromisoformat(data['rsvp_deadline']) if data.get('rsvp_deadline') else None,
            template_key=data.get('template_key', 'classic_01'),
            hero_image_url=data.get('hero_image_url'),
            image_1_url=data.get('image_1_url'),
            image_2_url=data.get('image_2_url'),
            video_url=data.get('video_url'),
            is_published=True,
        )

        db.session.add(invitation)
        db.session.flush()  # para tener unique_code

        invitation.share_url = _build_public_share_url(invitation)

        db.session.commit()

        return jsonify({
            'message': 'Invitación creada y publicada',
            'invitation': invitation.to_dict(),
            'share_url': invitation.share_url,
        }), 201

    except ValueError as e:
        db.session.rollback()
        return jsonify({'message': f'Formato de fecha inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear invitación: {str(e)}'}), 500


@invitations_bp.route('', methods=['GET'])
@jwt_required()
def list_invitations():
    """
    Listar invitaciones del usuario actual
    ---
    tags:
      - invitations
    security:
      - Bearer: []
    parameters:
      - in: query
        name: page
        type: integer
        required: false
        default: 1
      - in: query
        name: per_page
        type: integer
        required: false
        default: 10
    responses:
      200:
        description: Lista de invitaciones
    """
    user_id = get_jwt_identity()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    invitations = Invitation.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'invitations': [inv.to_dict() for inv in invitations.items],
        'total': invitations.total,
        'pages': invitations.pages,
        'current_page': page
    }), 200

@invitations_bp.route('/<int:invitation_id>', methods=['GET'])
@jwt_required()
def get_invitation(invitation_id):
    """
    Obtener detalles de una invitacion
    ---
    tags:
      - invitations
    security:
      - Bearer: []
    parameters:
      - in: path
        name: invitation_id
        required: true
        type: integer
    responses:
      200:
        description: Invitacion encontrada
      404:
        description: Invitacion no encontrada
    """
    user_id = get_jwt_identity()
    invitation = Invitation.query.get(invitation_id)
    
    if not invitation or invitation.user_id != user_id:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    return jsonify(invitation.to_dict()), 200

@invitations_bp.route('/<int:invitation_id>', methods=['PUT'])
@jwt_required()
def update_invitation(invitation_id):
    """
    Actualizar invitacion
    ---
    tags:
      - invitations
    security:
      - Bearer: []
    parameters:
      - in: path
        name: invitation_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            birthday_name:
              type: string
            birthday_age:
              type: integer
            event_title:
              type: string
            event_time:
              type: string
            event_location:
              type: string
            event_address:
              type: string
            organizer_name:
              type: string
            organizer_phone:
              type: string
            organizer_email:
              type: string
            dress_code:
              type: string
            special_notes:
              type: string
            birthday_date:
              type: string
              example: "2005-03-15T00:00:00"
            event_date:
              type: string
              example: "2024-03-16T19:00:00"
            rsvp_deadline:
              type: string
              example: "2024-03-12T23:59:59"
    responses:
      200:
        description: Invitacion actualizada
      400:
        description: Datos invalidos
      404:
        description: Invitacion no encontrada
      500:
        description: Error al actualizar invitacion
    """
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
            'organizer_email', 'dress_code', 'special_notes',
            'template_key', 'hero_image_url', 'image_1_url', 'image_2_url', 'video_url'
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
            'invitation': invitation.to_dict()
        }), 200
    
    except ValueError as e:
        return jsonify({'message': f'Formato de fecha inválido: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al actualizar invitación: {str(e)}'}), 500

@invitations_bp.route('/<int:invitation_id>', methods=['DELETE'])
@jwt_required()
def delete_invitation(invitation_id):
    """
    Eliminar invitacion
    ---
    tags:
      - invitations
    security:
      - Bearer: []
    parameters:
      - in: path
        name: invitation_id
        required: true
        type: integer
    responses:
      200:
        description: Invitacion eliminada
      404:
        description: Invitacion no encontrada
    """
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
    """
    Publicar invitacion
    ---
    tags:
      - invitations
    security:
      - Bearer: []
    parameters:
      - in: path
        name: invitation_id
        required: true
        type: integer
    responses:
      200:
        description: Invitacion publicada
      404:
        description: Invitacion no encontrada
    """
    user_id = get_jwt_identity()
    invitation = Invitation.query.get(invitation_id)
    
    if not invitation or invitation.user_id != user_id:
        return jsonify({'message': 'Invitación no encontrada'}), 404
    
    invitation.is_published = True
    invitation.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Invitación publicada exitosamente',
        'invitation': invitation.to_dict(),
        'share_url': invitation.share_url
    }), 200


@invitations_bp.route('/<int:invitation_id>/guests', methods=['GET'])
@jwt_required()
def list_invitation_guests(invitation_id):
    """Listar RSVPs (registro de asistencia) de una invitación del usuario.
    ---
    tags:
      - invitations
    security:
      - Bearer: []
    parameters:
      - in: path
        name: invitation_id
        required: true
        type: integer
    responses:
      200:
        description: Lista de RSVPs
      404:
        description: Invitacion no encontrada
    """
    user_id = get_jwt_identity()
    invitation = Invitation.query.get(invitation_id)

    if not invitation or invitation.user_id != user_id:
        return jsonify({'message': 'Invitación no encontrada'}), 404

    guests = [g.to_dict() for g in invitation.guests]

    return jsonify({
        'invitation_id': invitation.id,
        'rsvp_stats': invitation.rsvp_stats(),
        'guests': guests,
    }), 200
