from dataclasses import dataclass
from datetime import date
from typing import Optional, List

@dataclass
class Rutina:
    id: Optional[int]
    cliente_id: int
    titulo: str
    descripcion: str
    ejercicios: str  # Formato: "Ejercicio1: 3x12, Ejercicio2: 4x10"
    fecha_asignacion: date
    activa: bool = True
    
    def desactivar(self):
        """Desactiva la rutina"""
        self.activa = False
    
    def activar(self):
        """Activa la rutina"""
        self.activa = True
    
    def __repr__(self):
        return f"<Rutina {self.id} - {self.titulo} - Cliente: {self.cliente_id}>"