from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.usuario import Usuario

class UsuarioRepositorio(ABC):
    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def obtener_por_username(self, username: str) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Usuario]:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass