from datetime import date
from src.domain.entities.cliente import Cliente, Membresia, TipoMembresia

def test_cliente_se_crea_activo():
    cliente = Cliente(
        id=None, nombre="Juan", apellido="Pérez",
        dni="12345678", email="juan@email.com",
        telefono="555-1234", fecha_registro=date.today()
    )
    assert cliente.activo == True

def test_cliente_desactivar():
    cliente = Cliente(
        id=None, nombre="Juan", apellido="Pérez",
        dni="12345678", email="juan@email.com",
        telefono="555-1234", fecha_registro=date.today()
    )
    cliente.desactivar()
    assert cliente.activo == False

def test_membresia_calcula_vencimiento():
    membresia = Membresia(
        id=1, tipo=TipoMembresia.BASICA,
        precio=500.0, descripcion="Plan básico",
        duracion_dias=30
    )
    inicio = date(2026, 1, 1)
    vencimiento = membresia.calcular_vencimiento(inicio)
    assert vencimiento == date(2026, 1, 31)

def test_cliente_sin_membresia_no_tiene_membresia_activa():
    cliente = Cliente(
        id=None, nombre="Juan", apellido="Pérez",
        dni="12345678", email="juan@email.com",
        telefono="555-1234", fecha_registro=date.today()
    )
    assert cliente.tiene_membresia_activa() == False