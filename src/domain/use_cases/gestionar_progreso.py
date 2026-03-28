from datetime import date
from typing import List, Optional
from src.domain.entities.progreso import Progreso
from src.domain.interfaces.repositorios.progreso_repositorio import ProgresoRepositorio
from src.domain.interfaces.repositorios.cliente_repositorio import ClienteRepositorio

class GestionarProgreso:
    """
    Caso de uso: Gestión del progreso físico de clientes.
    
    Responsabilidades:
    - Registrar medidas periódicas
    - Consultar historial de progreso
    - Calcular evolución
    """
    
    def __init__(self, 
                 progreso_repo: ProgresoRepositorio,
                 cliente_repo: ClienteRepositorio):
        self.progreso_repo = progreso_repo
        self.cliente_repo = cliente_repo
    
    def registrar_medidas(self,
                          cliente_id: int,
                          peso: float = None,
                          altura: float = None,
                          brazos: float = None,
                          pecho: float = None,
                          cintura: float = None,
                          piernas: float = None,
                          notas: str = None) -> Progreso:
        """
        Registra nuevas medidas para un cliente.
        
        Args:
            cliente_id: ID del cliente
            peso: Peso en kg
            altura: Altura en cm
            brazos: Medida de brazos en cm
            pecho: Medida de pecho en cm
            cintura: Medida de cintura en cm
            piernas: Medida de piernas en cm
            notas: Notas adicionales
        
        Returns:
            Progreso: El registro creado
            
        Raises:
            ValueError: Si el cliente no existe
        """
        # Verificar que el cliente existe
        cliente = self.cliente_repo.obtener_por_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente {cliente_id} no encontrado")
        
        # Crear registro de progreso
        progreso = Progreso(
            id=None,
            cliente_id=cliente_id,
            fecha=date.today(),
            peso=peso,
            altura=altura,
            brazos=brazos,
            pecho=pecho,
            cintura=cintura,
            piernas=piernas,
            notas=notas
        )
        
        return self.progreso_repo.guardar(progreso)
    
    def obtener_progreso(self, id: int) -> Optional[Progreso]:
        """Obtiene un registro de progreso por su ID"""
        return self.progreso_repo.obtener_por_id(id)
    
    def obtener_historial_cliente(self, cliente_id: int) -> List[Progreso]:
        """Obtiene todo el historial de progreso de un cliente"""
        return self.progreso_repo.obtener_por_cliente(cliente_id)
    
    def obtener_ultimo_registro(self, cliente_id: int) -> Optional[Progreso]:
        """Obtiene el último registro de progreso de un cliente"""
        return self.progreso_repo.obtener_ultimo_por_cliente(cliente_id)
    
    def listar_todos(self) -> List[Progreso]:
        """Lista todos los registros de progreso"""
        return self.progreso_repo.listar_todos()
    
    def eliminar_registro(self, id: int) -> bool:
        """Elimina un registro de progreso"""
        return self.progreso_repo.eliminar(id)
    
    def calcular_evolucion(self, cliente_id: int) -> dict:
        """
        Calcula la evolución de un cliente entre el primer y último registro.
        
        Returns:
            dict: Diccionario con las diferencias de cada medida
        """
        historial = self.progreso_repo.obtener_por_cliente(cliente_id)
        if len(historial) < 2:
            return {"mensaje": "Se necesitan al menos 2 registros para calcular evolución"}
        
        primero = historial[-1]  # El más antiguo
        ultimo = historial[0]     # El más reciente
        
        evolucion = {}
        
        if primero.peso and ultimo.peso:
            evolucion['peso'] = ultimo.peso - primero.peso
        
        if primero.brazos and ultimo.brazos:
            evolucion['brazos'] = ultimo.brazos - primero.brazos
        
        if primero.pecho and ultimo.pecho:
            evolucion['pecho'] = ultimo.pecho - primero.pecho
        
        if primero.cintura and ultimo.cintura:
            evolucion['cintura'] = ultimo.cintura - primero.cintura
        
        if primero.piernas and ultimo.piernas:
            evolucion['piernas'] = ultimo.piernas - primero.piernas
        
        return {
            'primer_registro': primero.fecha.isoformat(),
            'ultimo_registro': ultimo.fecha.isoformat(),
            'evolucion': evolucion
        }