from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional
from enum import Enum

class TipoMembresia(Enum):
    BASICA = 'BÁSICA'
    VIP = 'VIP'
    PREMIUM = 'PREMIUM'

@dataclass
class Membresia:
    id: Optional[int]
    tipo: TipoMembresia
    precio: float
    descripcion: str
    duracion_dias: int = 30
    
    def calcular_vencimiento(self, fecha_inicio: date) -> date:
        return fecha_inicio + timedelta(days=self.duracion_dias)

@dataclass
class Cliente:
    id: Optional[int]
    nombre: str
    apellido: str
    dni: str
    email: Optional[str]
    telefono: Optional[str]
    fecha_registro: date
    activo: bool = True
    membresia_id: Optional[int] = None
    membresia: Optional[Membresia] = None
    fecha_vencimiento_membresia: Optional[date] = None
    
    def activar(self):
        self.activo = True
    
    def desactivar(self):
        self.activo = False
    
    def asignar_membresia(self, membresia: Membresia):
        self.membresia = membresia
        self.membresia_id = membresia.id
        self.fecha_vencimiento_membresia = membresia.calcular_vencimiento(date.today())
    
    def tiene_membresia_activa(self) -> bool:
        if not self.membresia or not self.fecha_vencimiento_membresia:
            return False
        return self.fecha_vencimiento_membresia >= date.today() and self.activo