from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='paciente')  # 'paciente' ou 'administrador'
    telefone = db.Column(db.String(20), nullable=True)
    idade = db.Column(db.Integer, nullable=True)
    family_id = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'<User {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'cpf': self.cpf,
            'avatar': self.avatar,
            'user_type': self.user_type,
            'telefone': self.telefone,
            'idade': self.idade,
            'family_id': self.family_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

