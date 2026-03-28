from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MembresiaModel(Base):
    __tablename__ = 'membresias'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(20), nullable=False, unique=True)
    precio = Column(Float, nullable=False)
    descripcion = Column(Text)
    duracion_dias = Column(Integer, default=30)
    
    # Solo relación con clientes
    clientes = relationship("ClienteModel", back_populates="membresia")

class ClienteModel(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    dni = Column(String(15), nullable=False, unique=True)
    email = Column(String(100))
    telefono = Column(String(20))
    fecha_registro = Column(Date, nullable=False)
    activo = Column(Boolean, default=True)
    membresia_id = Column(Integer, ForeignKey('membresias.id'))
    fecha_vencimiento_membresia = Column(Date)
    
    # SOLO relación con membresía, NO con pagos
    membresia = relationship("MembresiaModel", back_populates="clientes")
    
    # Eliminamos la relación con pagos para evitar el problema circular
    # Los pagos se manejarán desde el repositorio