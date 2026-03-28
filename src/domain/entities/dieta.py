from dataclasses import dataclass
from datetime import date
from typing import Optional, List

@dataclass
class Dieta:
    id: Optional[int]
    cliente_id: int
    titulo: str
    descripcion: str
    comidas: str  # Desayuno, Almuerzo, Cena, Snacks
    fecha_asignacion: date
    activa: bool = True
    
    def desactivar(self):
        """Desactiva la dieta"""
        self.activa = False
    
    def activar(self):
        """Activa la dieta"""
        self.activa = True
    
    def __repr__(self):
        return f"<Dieta {self.id} - {self.titulo} - Cliente: {self.cliente_id}>"