# Importar en orden correcto - PRIMERO ClienteModel
from .cliente_model import ClienteModel, MembresiaModel
from .pago_model import PagoModel
from .rutina_model import RutinaModel      # Después de ClienteModel
from .dieta_model import DietaModel
from .progreso_model import ProgresoModel

__all__ = [
    'ClienteModel',
    'MembresiaModel',
    'PagoModel',
    'RutinaModel',
    'DietaModel',
    'ProgresoModel'
]