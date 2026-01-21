from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    """Modelo de usuario (administrador)"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    invitations = db.relationship('Invitation', backref='user', lazy=True, cascade='all, delete-orphan')
    templates = db.relationship('Template', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Encriptar y guardar contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'email': self.email,
            'company_name': self.company_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
