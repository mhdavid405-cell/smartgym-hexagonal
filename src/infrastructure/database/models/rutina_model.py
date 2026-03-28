from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RutinaModel(Base):
    __tablename__ = 'rutinas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text)
    ejercicios = Column(Text)
    fecha_asignacion = Column(Date, nullable=False)
    activa = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)