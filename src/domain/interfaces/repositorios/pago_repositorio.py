from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.pago import Pago

class PagoRepositorio(ABC):
    @abstractmethod
    def guardar(self, pago: Pago) -> Pago:
        """Guarda un pago (crear o actualizar)"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Pago]:
        """Obtiene un pago por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_cliente(self, cliente_id: int) -> List[Pago]:
        """Obtiene todos los pagos de un cliente"""
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Pago]:
        """Lista todos los pagos del sistema"""
        pass