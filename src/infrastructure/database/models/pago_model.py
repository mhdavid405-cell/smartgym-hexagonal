from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PagoModel(Base):
    __tablename__ = 'pagos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    membresia_id = Column(Integer, ForeignKey('membresias.id'), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_pago = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    metodo_pago = Column(String(20), default='EFECTIVO')
    estado = Column(String(15), default='COMPLETADO')
    created_at = Column(DateTime, default=datetime.now)
    
    # Eliminamos todas las relaciones para evitar problemas circulares
    # Las consultas se harán directamente desde el repositorio