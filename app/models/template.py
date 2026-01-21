from app import db
from datetime import datetime

class Template(db.Model):
    """Modelo de template de invitación personalizable"""
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    # Textos personalizables
    title = db.Column(db.String(255), default='¡Te invitamos a celebrar!')
    subtitle = db.Column(db.String(255), default='Un día especial')
    header_text = db.Column(db.Text, default='')
    footer_text = db.Column(db.Text, default='')
    
    # Colores y estilos
    primary_color = db.Column(db.String(7), default='#FF69B4')  # Rosa por defecto
    secondary_color = db.Column(db.String(7), default='#FFD700')  # Oro
    text_color = db.Column(db.String(7), default='#333333')
    background_color = db.Column(db.String(7), default='#FFFFFF')
    
    # Imagenes/Archivos
    logo_url = db.Column(db.String(500))
    background_image_url = db.Column(db.String(500))
    
    # Estado
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    invitations = db.relationship('Invitation', backref='template', lazy=True)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'title': self.title,
            'subtitle': self.subtitle,
            'header_text': self.header_text,
            'footer_text': self.footer_text,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'text_color': self.text_color,
            'background_color': self.background_color,
            'logo_url': self.logo_url,
            'background_image_url': self.background_image_url,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
