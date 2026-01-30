from app import db
from datetime import datetime
import secrets


class Invitation(db.Model):
    """Modelo de invitación de cumpleaños.

    Nota: este proyecto usa db.create_all() (sin migraciones). Si agregás columnas,
    en dev puede que tengas que borrar el .db de SQLite y reiniciar.
    """

    __tablename__ = 'invitations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Información del cumpleañero
    birthday_name = db.Column(db.String(255), nullable=False)
    birthday_date = db.Column(db.DateTime, nullable=False)
    birthday_age = db.Column(db.Integer)

    # Información de la fiesta
    event_title = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_time = db.Column(db.String(10))  # HH:MM
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

    # Template / diseño + media (para landing pública)
    template_key = db.Column(db.String(64), default='classic_01')
    hero_image_url = db.Column(db.String(1000))
    image_1_url = db.Column(db.String(1000))
    image_2_url = db.Column(db.String(1000))
    video_url = db.Column(db.String(1000))

    # URL única para compartir
    unique_code = db.Column(db.String(32), unique=True, default=lambda: secrets.token_urlsafe(16))
    share_url = db.Column(db.String(500))

    # Configuración
    is_active = db.Column(db.Boolean, default=True)
    is_published = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    guests = db.relationship('Guest', backref='invitation', lazy=True, cascade='all, delete-orphan')

    def rsvp_stats(self):
        accepted = sum(1 for g in self.guests if g.rsvp_status == 'accepted')
        declined = sum(1 for g in self.guests if g.rsvp_status == 'declined')
        tentative = sum(1 for g in self.guests if g.rsvp_status == 'tentative')
        pending = sum(1 for g in self.guests if g.rsvp_status == 'pending')
        return {
            'accepted': accepted,
            'declined': declined,
            'tentative': tentative,
            'pending': pending,
            'total_rsvps': len(self.guests),
        }

    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
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
            'template_key': self.template_key,
            'hero_image_url': self.hero_image_url,
            'image_1_url': self.image_1_url,
            'image_2_url': self.image_2_url,
            'video_url': self.video_url,
            'unique_code': self.unique_code,
            'share_url': self.share_url,
            'is_active': self.is_active,
            'is_published': self.is_published,
            'rsvp_stats': self.rsvp_stats(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
