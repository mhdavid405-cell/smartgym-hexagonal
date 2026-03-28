from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.cliente import Cliente

class ClienteRepositorio(ABC):
    @abstractmethod
    def guardar(self, cliente: Cliente) -> Cliente:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    def obtener_por_dni(self, dni: str) -> Optional[Cliente]:
        pass
    
    @abstractmethod
    def listar_todos(self, solo_activos: bool = False) -> List[Cliente]:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
