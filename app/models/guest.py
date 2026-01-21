from app import db
from datetime import datetime

class Guest(db.Model):
    """Modelo de invitado"""
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    invitation_id = db.Column(db.Integer, db.ForeignKey('invitations.id'), nullable=False)
    
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    
    # RSVP
    rsvp_status = db.Column(db.String(20), default='pending')  # pending, accepted, declined, tentative
    rsvp_date = db.Column(db.DateTime)
    number_of_guests = db.Column(db.Integer, default=1)
    dietary_restrictions = db.Column(db.Text)
    
    # Notas
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'invitation_id': self.invitation_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'rsvp_status': self.rsvp_status,
            'rsvp_date': self.rsvp_date.isoformat() if self.rsvp_date else None,
            'number_of_guests': self.number_of_guests,
            'dietary_restrictions': self.dietary_restrictions,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
