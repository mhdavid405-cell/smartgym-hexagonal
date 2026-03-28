from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.cliente import Membresia

class MembresiaRepositorio(ABC):
    """
    Puerto: Contrato que debe cumplir cualquier repositorio de membresías.
    
    Define las operaciones necesarias para persistir y recuperar
    membresías, independientemente de la tecnología de base de datos.
    """
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Membresia]:
        """Obtiene una membresía por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_tipo(self, tipo: str) -> Optional[Membresia]:
        """Obtiene una membresía por su tipo (BÁSICA, VIP, PREMIUM)"""
        pass
    
    @abstractmethod
    def listar_todas(self) -> List[Membresia]:
        """Lista todas las membresías disponibles"""
        pass
    
    @abstractmethod
    def guardar(self, membresia: Membresia) -> Membresia:
        """Guarda una membresía (crear o actualizar)"""
        pass