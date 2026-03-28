from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Pago:
    id: Optional[int]
    cliente_id: int
    membresia_id: int
    monto: float
    fecha_pago: date
    fecha_vencimiento: date
    metodo_pago: str = 'EFECTIVO'
    estado: str = 'COMPLETADO'
    
    def validar_monto(self, precio_membresia: float) -> bool:
        """Regla de negocio: validar que el monto pagado sea correcto"""
        return self.monto == precio_membresia
    
    def cancelar(self):
        """Regla de negocio: cancelar pago"""
        self.estado = 'CANCELADO'
    
    def __repr__(self):
        return f"<Pago {self.id} - Cliente {self.cliente_id} - ${self.monto}>"