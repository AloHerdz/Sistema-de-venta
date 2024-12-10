# app/models/transaccion.py
from .base import db
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Transaccion(db.Model):
    __tablename__ = 'transacciones'

    id_transaccion = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    monto = Column(Float, nullable=False)
    tipo = Column(String(1), nullable=False)  # '+' o '-'
    fecha = Column(DateTime, default=datetime.utcnow)

    # Relación con cliente
    cliente = relationship("Cliente", backref="transacciones")

    def to_dict(self):
        return {
            "id_transaccion": self.id_transaccion,
            "id_cliente": self.id_cliente,
            "monto": self.monto,
            "tipo": self.tipo,
            "fecha": self.fecha.isoformat()
        }
