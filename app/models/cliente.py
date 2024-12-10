# app/models/cliente.py
from .base import db
from sqlalchemy import Column, Integer, String

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(50), nullable=False)
    colonia = Column(String(100))

    def to_dict(self):
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "colonia": self.colonia
        }