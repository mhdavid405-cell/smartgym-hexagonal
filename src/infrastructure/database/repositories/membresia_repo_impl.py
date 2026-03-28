from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.entities.cliente import Membresia, TipoMembresia
from src.domain.interfaces.repositorios.membresia_repositorio import MembresiaRepositorio
from src.infrastructure.database.models.cliente_model import MembresiaModel

class MembresiaRepositorioSQLServer(MembresiaRepositorio):
    """
    Implementación concreta del repositorio de membresías para SQL Server.
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def _model_to_entity(self, modelo: MembresiaModel) -> Membresia:
        """Convierte modelo SQLAlchemy a entidad de dominio"""
        return Membresia(
            id=modelo.id,
            tipo=TipoMembresia(modelo.tipo),
            precio=modelo.precio,
            descripcion=modelo.descripcion,
            duracion_dias=modelo.duracion_dias
        )
    
    def _entity_to_model(self, membresia: Membresia) -> MembresiaModel:
        """Convierte entidad de dominio a modelo SQLAlchemy"""
        return MembresiaModel(
            id=membresia.id,
            tipo=membresia.tipo.value,
            precio=membresia.precio,
            descripcion=membresia.descripcion,
            duracion_dias=membresia.duracion_dias
        )
    
    def obtener_por_id(self, id: int) -> Optional[Membresia]:
        """Obtiene una membresía por su ID"""
        modelo = self.session.query(MembresiaModel).filter(MembresiaModel.id == id).first()
        return self._model_to_entity(modelo) if modelo else None
    
    def obtener_por_tipo(self, tipo: str) -> Optional[Membresia]:
        """Obtiene una membresía por su tipo"""
        modelo = self.session.query(MembresiaModel).filter(
            MembresiaModel.tipo == tipo.upper()
        ).first()
        return self._model_to_entity(modelo) if modelo else None
    
    def listar_todas(self) -> List[Membresia]:
        """Lista todas las membresías disponibles"""
        modelos = self.session.query(MembresiaModel).all()
        return [self._model_to_entity(m) for m in modelos]
    
    def guardar(self, membresia: Membresia) -> Membresia:
        """Guarda una membresía"""
        modelo = self._entity_to_model(membresia)
        
        if membresia.id:
            self.session.merge(modelo)
        else:
            self.session.add(modelo)
        
        self.session.commit()
        
        if not membresia.id:
            membresia.id = modelo.id
        
        return membresia