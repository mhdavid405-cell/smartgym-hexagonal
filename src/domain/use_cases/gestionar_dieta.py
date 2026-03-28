from datetime import date
from typing import List, Optional
from src.domain.entities.dieta import Dieta
from src.domain.interfaces.repositorios.dieta_repositorio import DietaRepositorio
from src.domain.interfaces.repositorios.cliente_repositorio import ClienteRepositorio

class GestionarDieta:
    """
    Caso de uso: Gestión de dietas alimenticias.
    
    Responsabilidades:
    - Asignar dietas a clientes
    - Consultar dietas por cliente
    - Activar/desactivar dietas
    - Listar todas las dietas
    """
    
    def __init__(self, 
                 dieta_repo: DietaRepositorio,
                 cliente_repo: ClienteRepositorio):
        self.dieta_repo = dieta_repo
        self.cliente_repo = cliente_repo
    
    def asignar_dieta(self, 
                      cliente_id: int, 
                      titulo: str,
                      descripcion: str,
                      comidas: str) -> Dieta:
        """
        Asigna una nueva dieta a un cliente.
        
        Args:
            cliente_id: ID del cliente
            titulo: Título de la dieta
            descripcion: Descripción general
            comidas: Plan de comidas
        
        Returns:
            Dieta: La dieta creada
            
        Raises:
            ValueError: Si el cliente no existe
        """
        # Verificar que el cliente existe
        cliente = self.cliente_repo.obtener_por_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente {cliente_id} no encontrado")
        
        # Desactivar dieta anterior si existe
        dieta_anterior = self.dieta_repo.obtener_activa_por_cliente(cliente_id)
        if dieta_anterior:
            dieta_anterior.desactivar()
            self.dieta_repo.guardar(dieta_anterior)
        
        # Crear nueva dieta
        dieta = Dieta(
            id=None,
            cliente_id=cliente_id,
            titulo=titulo,
            descripcion=descripcion,
            comidas=comidas,
            fecha_asignacion=date.today(),
            activa=True
        )
        
        return self.dieta_repo.guardar(dieta)
    
    def obtener_dieta(self, id: int) -> Optional[Dieta]:
        """Obtiene una dieta por su ID"""
        return self.dieta_repo.obtener_por_id(id)
    
    def obtener_dietas_cliente(self, cliente_id: int) -> List[Dieta]:
        """Obtiene todas las dietas de un cliente"""
        return self.dieta_repo.obtener_por_cliente(cliente_id)
    
    def obtener_dieta_activa(self, cliente_id: int) -> Optional[Dieta]:
        """Obtiene la dieta activa de un cliente"""
        return self.dieta_repo.obtener_activa_por_cliente(cliente_id)
    
    def listar_todas(self) -> List[Dieta]:
        """Lista todas las dietas del sistema"""
        return self.dieta_repo.listar_todas()
    
    def desactivar_dieta(self, id: int) -> bool:
        """Desactiva una dieta"""
        dieta = self.dieta_repo.obtener_por_id(id)
        if not dieta:
            raise ValueError(f"Dieta {id} no encontrada")
        
        dieta.desactivar()
        self.dieta_repo.guardar(dieta)
        return True
    
    def eliminar_dieta(self, id: int) -> bool:
        """Elimina una dieta (solo si es necesario)"""
        return self.dieta_repo.eliminar(id)