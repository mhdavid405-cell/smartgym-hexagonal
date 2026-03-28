from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.domain.entities.usuario import Usuario, RolUsuario
from src.domain.interfaces.repositorios.usuario_repositorio import UsuarioRepositorio
from src.infrastructure.database.models.usuario_model import UsuarioModel
import bcrypt

class UsuarioRepositorioSQLServer(UsuarioRepositorio):
    def __init__(self, session: Session):
        self.session = session
    
    def _model_to_entity(self, modelo: UsuarioModel) -> Usuario:
        return Usuario(
            id=modelo.id,
            username=modelo.username,
            email=modelo.email,
            password_hash=modelo.password_hash,
            rol=RolUsuario(modelo.rol),
            cliente_id=modelo.cliente_id,
            activo=modelo.activo,
            created_at=modelo.created_at,
            updated_at=modelo.updated_at
        )
    
    def _entity_to_model(self, usuario: Usuario) -> UsuarioModel:
        return UsuarioModel(
            id=usuario.id,
            username=usuario.username,
            email=usuario.email,
            password_hash=usuario.password_hash,
            rol=usuario.rol.value,
            cliente_id=usuario.cliente_id,
            activo=usuario.activo
        )
    
    def guardar(self, usuario: Usuario) -> Usuario:
        modelo = self._entity_to_model(usuario)
        
        if usuario.id:
            self.session.merge(modelo)
        else:
            self.session.add(modelo)
        
        self.session.commit()
        
        if not usuario.id:
            usuario.id = modelo.id
        
        return usuario
    
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        modelo = self.session.query(UsuarioModel).filter(UsuarioModel.id == id).first()
        return self._model_to_entity(modelo) if modelo else None
    
    def obtener_por_username(self, username: str) -> Optional[Usuario]:
        modelo = self.session.query(UsuarioModel).filter(UsuarioModel.username == username).first()
        return self._model_to_entity(modelo) if modelo else None
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        modelo = self.session.query(UsuarioModel).filter(UsuarioModel.email == email).first()
        return self._model_to_entity(modelo) if modelo else None
    
    def listar_todos(self) -> List[Usuario]:
        modelos = self.session.query(UsuarioModel).all()
        return [self._model_to_entity(m) for m in modelos]
    
    def eliminar(self, id: int) -> bool:
        usuario = self.session.query(UsuarioModel).filter(UsuarioModel.id == id).first()
        if not usuario:
            return False
        self.session.delete(usuario)
        self.session.commit()
        return True