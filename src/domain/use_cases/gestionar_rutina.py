from datetime import date
from typing import List, Optional
from src.domain.entities.rutina import Rutina
from src.domain.interfaces.repositorios.rutina_repositorio import RutinaRepositorio
from src.domain.interfaces.repositorios.cliente_repositorio import ClienteRepositorio

class GestionarRutina:
    """
    Caso de uso: Gestión de rutinas de entrenamiento.
    
    Responsabilidades:
    - Asignar rutinas a clientes
    - Consultar rutinas por cliente
    - Activar/desactivar rutinas
    - Listar todas las rutinas
    """
    
    def __init__(self, 
                 rutina_repo: RutinaRepositorio,
                 cliente_repo: ClienteRepositorio):
        self.rutina_repo = rutina_repo
        self.cliente_repo = cliente_repo
    
    def asignar_rutina(self, 
                       cliente_id: int, 
                       titulo: str,
                       descripcion: str,
                       ejercicios: str) -> Rutina:
        """
        Asigna una nueva rutina a un cliente.
        
        Args:
            cliente_id: ID del cliente
            titulo: Título de la rutina
            descripcion: Descripción general
            ejercicios: Lista de ejercicios
        
        Returns:
            Rutina: La rutina creada
            
        Raises:
            ValueError: Si el cliente no existe
        """
        # Verificar que el cliente existe
        cliente = self.cliente_repo.obtener_por_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente {cliente_id} no encontrado")
        
        # Desactivar rutina anterior si existe
        rutina_anterior = self.rutina_repo.obtener_activa_por_cliente(cliente_id)
        if rutina_anterior:
            rutina_anterior.desactivar()
            self.rutina_repo.guardar(rutina_anterior)
        
        # Crear nueva rutina
        rutina = Rutina(
            id=None,
            cliente_id=cliente_id,
            titulo=titulo,
            descripcion=descripcion,
            ejercicios=ejercicios,
            fecha_asignacion=date.today(),
            activa=True
        )
        
        return self.rutina_repo.guardar(rutina)
    
    def obtener_rutina(self, id: int) -> Optional[Rutina]:
        """Obtiene una rutina por su ID"""
        return self.rutina_repo.obtener_por_id(id)
    
    def obtener_rutinas_cliente(self, cliente_id: int) -> List[Rutina]:
        """Obtiene todas las rutinas de un cliente"""
        return self.rutina_repo.obtener_por_cliente(cliente_id)
    
    def obtener_rutina_activa(self, cliente_id: int) -> Optional[Rutina]:
        """Obtiene la rutina activa de un cliente"""
        return self.rutina_repo.obtener_activa_por_cliente(cliente_id)
    
    def listar_todas(self) -> List[Rutina]:
        """Lista todas las rutinas del sistema"""
        return self.rutina_repo.listar_todas()
    
    def desactivar_rutina(self, id: int) -> bool:
        """Desactiva una rutina"""
        rutina = self.rutina_repo.obtener_por_id(id)
        if not rutina:
            raise ValueError(f"Rutina {id} no encontrada")
        
        rutina.desactivar()
        self.rutina_repo.guardar(rutina)
        return True
    
    def eliminar_rutina(self, id: int) -> bool:
        """Elimina una rutina (solo si es necesario)"""
        return self.rutina_repo.eliminar(id)