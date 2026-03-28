from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.domain.entities.progreso import Progreso
from src.domain.interfaces.repositorios.progreso_repositorio import ProgresoRepositorio

class ProgresoRepositorioSQLServer(ProgresoRepositorio):
    def __init__(self, session: Session):
        self.session = session
    
    def guardar(self, progreso: Progreso) -> Progreso:
        """Guarda un registro de progreso usando SQL directo"""
        
        if progreso.id:
            # Actualizar
            sql = text("""
                UPDATE progreso 
                SET peso = :peso, 
                    altura = :altura,
                    brazos = :brazos,
                    pecho = :pecho,
                    cintura = :cintura,
                    piernas = :piernas,
                    notas = :notas
                WHERE id = :id
            """)
            self.session.execute(sql, {
                'id': progreso.id,
                'peso': progreso.peso,
                'altura': progreso.altura,
                'brazos': progreso.brazos,
                'pecho': progreso.pecho,
                'cintura': progreso.cintura,
                'piernas': progreso.piernas,
                'notas': progreso.notas
            })
        else:
            # Insertar nuevo
            sql = text("""
                INSERT INTO progreso (cliente_id, fecha, peso, altura, brazos, pecho, cintura, piernas, notas)
                OUTPUT INSERTED.id
                VALUES (:cliente_id, :fecha, :peso, :altura, :brazos, :pecho, :cintura, :piernas, :notas)
            """)
            result = self.session.execute(sql, {
                'cliente_id': progreso.cliente_id,
                'fecha': progreso.fecha,
                'peso': progreso.peso,
                'altura': progreso.altura,
                'brazos': progreso.brazos,
                'pecho': progreso.pecho,
                'cintura': progreso.cintura,
                'piernas': progreso.piernas,
                'notas': progreso.notas
            })
            progreso.id = result.fetchone()[0]
        
        self.session.commit()
        return progreso
    
    def obtener_por_id(self, id: int) -> Optional[Progreso]:
        sql = text("SELECT * FROM progreso WHERE id = :id")
        result = self.session.execute(sql, {'id': id}).first()
        
        if not result:
            return None
        
        return Progreso(
            id=result.id,
            cliente_id=result.cliente_id,
            fecha=result.fecha,
            peso=result.peso,
            altura=result.altura,
            brazos=result.brazos,
            pecho=result.pecho,
            cintura=result.cintura,
            piernas=result.piernas,
            notas=result.notas
        )
    
    def obtener_por_cliente(self, cliente_id: int) -> List[Progreso]:
        sql = text("""
            SELECT * FROM progreso 
            WHERE cliente_id = :cliente_id 
            ORDER BY fecha DESC
        """)
        resultados = self.session.execute(sql, {'cliente_id': cliente_id}).fetchall()
        
        return [
            Progreso(
                id=r.id,
                cliente_id=r.cliente_id,
                fecha=r.fecha,
                peso=r.peso,
                altura=r.altura,
                brazos=r.brazos,
                pecho=r.pecho,
                cintura=r.cintura,
                piernas=r.piernas,
                notas=r.notas
            ) for r in resultados
        ]
    
    def obtener_ultimo_por_cliente(self, cliente_id: int) -> Optional[Progreso]:
        sql = text("""
            SELECT TOP 1 * FROM progreso 
            WHERE cliente_id = :cliente_id 
            ORDER BY fecha DESC
        """)
        result = self.session.execute(sql, {'cliente_id': cliente_id}).first()
        
        if not result:
            return None
        
        return Progreso(
            id=result.id,
            cliente_id=result.cliente_id,
            fecha=result.fecha,
            peso=result.peso,
            altura=result.altura,
            brazos=result.brazos,
            pecho=result.pecho,
            cintura=result.cintura,
            piernas=result.piernas,
            notas=result.notas
        )
    
    def listar_todos(self) -> List[Progreso]:
        sql = text("SELECT * FROM progreso ORDER BY fecha DESC")
        resultados = self.session.execute(sql).fetchall()
        
        return [
            Progreso(
                id=r.id,
                cliente_id=r.cliente_id,
                fecha=r.fecha,
                peso=r.peso,
                altura=r.altura,
                brazos=r.brazos,
                pecho=r.pecho,
                cintura=r.cintura,
                piernas=r.piernas,
                notas=r.notas
            ) for r in resultados
        ]
    
    def eliminar(self, id: int) -> bool:
        sql = text("DELETE FROM progreso WHERE id = :id")
        result = self.session.execute(sql, {'id': id})
        self.session.commit()
        return result.rowcount > 0