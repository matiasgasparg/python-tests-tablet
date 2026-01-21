from app import db
from datetime import datetime
import secrets

class Invitation(db.Model):
    """Modelo de invitación de cumpleaños"""
    __tablename__ = 'invitations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))
    
    # Información del cumpleañero
    birthday_name = db.Column(db.String(255), nullable=False)
    birthday_date = db.Column(db.DateTime, nullable=False)
    birthday_age = db.Column(db.Integer)
    
    # Información de la fiesta
    event_title = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_time = db.Column(db.String(10))  # HH:MM formato
    event_location = db.Column(db.Text)
    event_address = db.Column(db.String(500))
    
    # Información del organizador
    organizer_name = db.Column(db.String(255))
    organizer_phone = db.Column(db.String(20))
    organizer_email = db.Column(db.String(120))
    
    # Detalles adicionales
    dress_code = db.Column(db.String(255))
    rsvp_deadline = db.Column(db.DateTime)
    special_notes = db.Column(db.Text)
    
    # URL única para compartir
    unique_code = db.Column(db.String(32), unique=True, default=lambda: secrets.token_urlsafe(16))
    share_url = db.Column(db.String(500))
    
    # Configuración de la invitación
    is_active = db.Column(db.Boolean, default=True)
    is_published = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    guests = db.relationship('Guest', backref='invitation', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'template_id': self.template_id,
            'birthday_name': self.birthday_name,
            'birthday_date': self.birthday_date.isoformat() if self.birthday_date else None,
            'birthday_age': self.birthday_age,
            'event_title': self.event_title,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'event_time': self.event_time,
            'event_location': self.event_location,
            'event_address': self.event_address,
            'organizer_name': self.organizer_name,
            'organizer_phone': self.organizer_phone,
            'organizer_email': self.organizer_email,
            'dress_code': self.dress_code,
            'rsvp_deadline': self.rsvp_deadline.isoformat() if self.rsvp_deadline else None,
            'special_notes': self.special_notes,
            'unique_code': self.unique_code,
            'share_url': self.share_url,
            'is_active': self.is_active,
            'is_published': self.is_published,
            'guests_count': len(self.guests),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def to_dict_with_template(self):
        """Incluir información del template"""
        data = self.to_dict()
        if self.template:
            data['template'] = self.template.to_dict()
        return data
