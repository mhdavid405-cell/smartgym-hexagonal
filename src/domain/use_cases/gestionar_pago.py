from datetime import date
from typing import List, Optional
from src.domain.entities.pago import Pago
from src.domain.interfaces.repositorios.pago_repositorio import PagoRepositorio
from src.domain.interfaces.repositorios.cliente_repositorio import ClienteRepositorio
from src.domain.interfaces.repositorios.membresia_repositorio import MembresiaRepositorio

class GestionarPago:
    """
    Caso de uso: Gestión de pagos del gimnasio.
    
    Responsabilidades:
    - Registrar nuevos pagos
    - Validar montos contra membresías
    - Actualizar membresía del cliente
    - Consultar historial de pagos
    """
    
    def __init__(self, 
                 pago_repo: PagoRepositorio,
                 cliente_repo: ClienteRepositorio,
                 membresia_repo: MembresiaRepositorio):
        """
        Inicializa el caso de uso con los repositorios necesarios.
        
        Args:
            pago_repo: Repositorio de pagos
            cliente_repo: Repositorio de clientes
            membresia_repo: Repositorio de membresías
        """
        self.pago_repo = pago_repo
        self.cliente_repo = cliente_repo
        self.membresia_repo = membresia_repo
    
    def registrar_pago(self, 
                       cliente_id: int, 
                       membresia_id: int, 
                       monto: float,
                       metodo_pago: str = 'EFECTIVO') -> Pago:
        """
        Registra un nuevo pago y actualiza la membresía del cliente.
        
        Args:
            cliente_id: ID del cliente que realiza el pago
            membresia_id: ID de la membresía que se paga
            monto: Monto pagado
            metodo_pago: Método de pago (EFECTIVO, TARJETA, TRANSFERENCIA)
        
        Returns:
            Pago: La entidad pago con su ID asignado
            
        Raises:
            ValueError: Si el cliente no existe, la membresía no existe,
                       o el monto no coincide con el precio de la membresía
        """
        # ========== VALIDACIONES ==========
        # Verificar que el cliente existe
        cliente = self.cliente_repo.obtener_por_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente {cliente_id} no encontrado")
        
        # Verificar que la membresía existe
        membresia = self.membresia_repo.obtener_por_id(membresia_id)
        if not membresia:
            raise ValueError(f"Membresía {membresia_id} no encontrada")
        
        # Validar que el monto sea correcto
        if monto != membresia.precio:
            raise ValueError(f"El monto debe ser ${membresia.precio} para la membresía {membresia.tipo}")
        
        # ========== PROCESAR PAGO ==========
        # Calcular fecha de vencimiento (30 días desde hoy)
        fecha_vencimiento = membresia.calcular_vencimiento(date.today())
        
        # Crear entidad pago
        pago = Pago(
            id=None,
            cliente_id=cliente_id,
            membresia_id=membresia_id,
            monto=monto,
            fecha_pago=date.today(),
            fecha_vencimiento=fecha_vencimiento,
            metodo_pago=metodo_pago
        )
        
        # Guardar pago
        pago_guardado = self.pago_repo.guardar(pago)
        
        # ========== ACTUALIZAR CLIENTE ==========
        # Asignar la nueva membresía al cliente
        cliente.asignar_membresia(membresia)
        self.cliente_repo.guardar(cliente)
        
        return pago_guardado
    
    def obtener_pagos_cliente(self, cliente_id: int) -> List[Pago]:
        """
        Obtiene el historial de pagos de un cliente.
        
        Args:
            cliente_id: ID del cliente
        
        Returns:
            List[Pago]: Lista de pagos del cliente ordenados por fecha
        """
        return self.pago_repo.obtener_por_cliente(cliente_id)
    
    def obtener_pago(self, pago_id: int) -> Optional[Pago]:
        """
        Obtiene un pago por su ID.
        
        Args:
            pago_id: ID del pago
        
        Returns:
            Optional[Pago]: El pago si existe, None si no
        """
        return self.pago_repo.obtener_por_id(pago_id)
    
    def listar_pagos(self) -> List[Pago]:
        """
        Lista todos los pagos del sistema.
        
        Returns:
            List[Pago]: Lista de todos los pagos
        """
        return self.pago_repo.listar_todos()