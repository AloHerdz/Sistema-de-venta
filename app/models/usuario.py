from .base import db
from sqlalchemy import Column, Integer, String

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "username": self.username
        }
