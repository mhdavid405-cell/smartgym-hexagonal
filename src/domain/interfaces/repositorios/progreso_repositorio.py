from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from src.domain.entities.progreso import Progreso

class ProgresoRepositorio(ABC):
    @abstractmethod
    def guardar(self, progreso: Progreso) -> Progreso:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Progreso]:
        pass
    
    @abstractmethod
    def obtener_por_cliente(self, cliente_id: int) -> List[Progreso]:
        pass
    
    @abstractmethod
    def obtener_ultimo_por_cliente(self, cliente_id: int) -> Optional[Progreso]:
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Progreso]:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass