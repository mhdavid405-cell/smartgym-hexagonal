from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Progreso:
    id: Optional[int]
    cliente_id: int
    fecha: date
    peso: Optional[float] = None
    altura: Optional[float] = None
    brazos: Optional[float] = None
    pecho: Optional[float] = None
    cintura: Optional[float] = None
    piernas: Optional[float] = None
    notas: Optional[str] = None
    
    def __repr__(self):
        return f"<Progreso {self.id} - Cliente: {self.cliente_id} - Fecha: {self.fecha}>"