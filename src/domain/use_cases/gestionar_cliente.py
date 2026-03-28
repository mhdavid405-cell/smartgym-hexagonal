from datetime import date
from typing import List, Optional
from src.domain.entities.cliente import Cliente
from src.domain.interfaces.repositorios.cliente_repositorio import ClienteRepositorio

class GestionarCliente:
    def __init__(self, cliente_repo: ClienteRepositorio):
        self.cliente_repo = cliente_repo
    
    def registrar_cliente(self, nombre: str, apellido: str, dni: str, 
                          email: str = None, telefono: str = None) -> Cliente:
        existente = self.cliente_repo.obtener_por_dni(dni)
        if existente:
            raise ValueError(f"Ya existe un cliente con DNI {dni}")
        
        cliente = Cliente(
            id=None,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email,
            telefono=telefono,
            fecha_registro=date.today()
        )
        
        return self.cliente_repo.guardar(cliente)
    
    def obtener_cliente(self, id: int) -> Optional[Cliente]:
        return self.cliente_repo.obtener_por_id(id)
    
    def listar_clientes(self, solo_activos: bool = False) -> List[Cliente]:
        return self.cliente_repo.listar_todos(solo_activos)
    
    def dar_de_baja(self, id: int) -> bool:
        cliente = self.cliente_repo.obtener_por_id(id)
        if not cliente:
            raise ValueError(f"Cliente {id} no encontrado")
        
        cliente.desactivar()
        self.cliente_repo.guardar(cliente)
        return True
