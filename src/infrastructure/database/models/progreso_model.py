from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProgresoModel(Base):
    __tablename__ = 'progreso'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    fecha = Column(Date, nullable=False)
    peso = Column(Float)
    altura = Column(Float)
    brazos = Column(Float)
    pecho = Column(Float)
    cintura = Column(Float)
    piernas = Column(Float)
    notas = Column(Text)