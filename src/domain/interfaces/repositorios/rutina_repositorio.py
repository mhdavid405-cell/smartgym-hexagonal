from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.rutina import Rutina

class RutinaRepositorio(ABC):
    @abstractmethod
    def guardar(self, rutina: Rutina) -> Rutina:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Rutina]:
        pass
    
    @abstractmethod
    def obtener_por_cliente(self, cliente_id: int) -> List[Rutina]:
        pass
    
    @abstractmethod
    def obtener_activa_por_cliente(self, cliente_id: int) -> Optional[Rutina]:
        pass
    
    @abstractmethod
    def listar_todas(self) -> List[Rutina]:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass