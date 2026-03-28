from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.dieta import Dieta

class DietaRepositorio(ABC):
    @abstractmethod
    def guardar(self, dieta: Dieta) -> Dieta:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Dieta]:
        pass
    
    @abstractmethod
    def obtener_por_cliente(self, cliente_id: int) -> List[Dieta]:
        pass
    
    @abstractmethod
    def obtener_activa_por_cliente(self, cliente_id: int) -> Optional[Dieta]:
        pass
    
    @abstractmethod
    def listar_todas(self) -> List[Dieta]:
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass