from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from src.domain.entities.cliente import Cliente, Membresia, TipoMembresia
from src.domain.interfaces.repositorios.cliente_repositorio import ClienteRepositorio
from src.infrastructure.database.models.cliente_model import ClienteModel, MembresiaModel

class ClienteRepositorioSQLServer(ClienteRepositorio):
    def __init__(self, session: Session):
        self.session = session
    
    def _model_to_entity(self, modelo: ClienteModel) -> Cliente:
        """Convierte modelo SQLAlchemy a entidad de dominio"""
        membresia_entity = None
        if modelo.membresia:
            membresia_entity = Membresia(
                id=modelo.membresia.id,
                tipo=TipoMembresia(modelo.membresia.tipo),
                precio=modelo.membresia.precio,
                descripcion=modelo.membresia.descripcion,
                duracion_dias=modelo.membresia.duracion_dias
            )
        
        return Cliente(
            id=modelo.id,
            nombre=modelo.nombre,
            apellido=modelo.apellido,
            dni=modelo.dni,
            email=modelo.email,
            telefono=modelo.telefono,
            fecha_registro=modelo.fecha_registro,
            activo=modelo.activo,
            membresia=membresia_entity,
            membresia_id=modelo.membresia_id,
            fecha_vencimiento_membresia=modelo.fecha_vencimiento_membresia
        )
    
    def _entity_to_model(self, cliente: Cliente) -> ClienteModel:
        """Convierte entidad de dominio a modelo SQLAlchemy"""
        return ClienteModel(
            id=cliente.id,
            nombre=cliente.nombre,
            apellido=cliente.apellido,
            dni=cliente.dni,
            email=cliente.email,
            telefono=cliente.telefono,
            fecha_registro=cliente.fecha_registro,
            activo=cliente.activo,
            membresia_id=cliente.membresia_id,
            fecha_vencimiento_membresia=cliente.fecha_vencimiento_membresia
        )
    
    def guardar(self, cliente: Cliente) -> Cliente:
        modelo = self._entity_to_model(cliente)
        
        if cliente.id:
            self.session.merge(modelo)
        else:
            self.session.add(modelo)
        
        self.session.commit()
        
        if not cliente.id:
            cliente.id = modelo.id
        
        return cliente
    
    def obtener_por_id(self, id: int) -> Optional[Cliente]:
        modelo = self.session.query(ClienteModel).filter(ClienteModel.id == id).first()
        return self._model_to_entity(modelo) if modelo else None
    
    def obtener_por_dni(self, dni: str) -> Optional[Cliente]:
        modelo = self.session.query(ClienteModel).filter(ClienteModel.dni == dni).first()
        return self._model_to_entity(modelo) if modelo else None
    
    def listar_todos(self, solo_activos: bool = False) -> List[Cliente]:
        query = self.session.query(ClienteModel)
        if solo_activos:
            query = query.filter(ClienteModel.activo == True)
        
        modelos = query.all()
        return [self._model_to_entity(m) for m in modelos]
    
    def eliminar(self, id: int) -> bool:
        cliente = self.session.query(ClienteModel).filter(ClienteModel.id == id).first()
        if not cliente:
            return False
        
        cliente.activo = False
        self.session.commit()
        return True