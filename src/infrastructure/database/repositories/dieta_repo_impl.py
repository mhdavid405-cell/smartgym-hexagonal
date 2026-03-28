from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.domain.entities.dieta import Dieta
from src.domain.interfaces.repositorios.dieta_repositorio import DietaRepositorio

class DietaRepositorioSQLServer(DietaRepositorio):
    def __init__(self, session: Session):
        self.session = session
    
    def guardar(self, dieta: Dieta) -> Dieta:
        """Guarda una dieta usando SQL directo para evitar problemas de mapeo"""
        
        if dieta.id:
            # Actualizar
            sql = text("""
                UPDATE dietas 
                SET titulo = :titulo, 
                    descripcion = :descripcion, 
                    comidas = :comidas,
                    activa = :activa
                WHERE id = :id
            """)
            self.session.execute(sql, {
                'id': dieta.id,
                'titulo': dieta.titulo,
                'descripcion': dieta.descripcion,
                'comidas': dieta.comidas,
                'activa': dieta.activa
            })
        else:
            # Insertar nuevo
            sql = text("""
                INSERT INTO dietas (cliente_id, titulo, descripcion, comidas, fecha_asignacion, activa)
                OUTPUT INSERTED.id
                VALUES (:cliente_id, :titulo, :descripcion, :comidas, :fecha_asignacion, :activa)
            """)
            result = self.session.execute(sql, {
                'cliente_id': dieta.cliente_id,
                'titulo': dieta.titulo,
                'descripcion': dieta.descripcion,
                'comidas': dieta.comidas,
                'fecha_asignacion': dieta.fecha_asignacion,
                'activa': dieta.activa
            })
            dieta.id = result.fetchone()[0]
        
        self.session.commit()
        return dieta
    
    def obtener_por_id(self, id: int) -> Optional[Dieta]:
        sql = text("SELECT * FROM dietas WHERE id = :id")
        result = self.session.execute(sql, {'id': id}).first()
        
        if not result:
            return None
        
        return Dieta(
            id=result.id,
            cliente_id=result.cliente_id,
            titulo=result.titulo,
            descripcion=result.descripcion,
            comidas=result.comidas,
            fecha_asignacion=result.fecha_asignacion,
            activa=result.activa
        )
    
    def obtener_por_cliente(self, cliente_id: int) -> List[Dieta]:
        sql = text("""
            SELECT * FROM dietas 
            WHERE cliente_id = :cliente_id 
            ORDER BY fecha_asignacion DESC
        """)
        resultados = self.session.execute(sql, {'cliente_id': cliente_id}).fetchall()
        
        return [
            Dieta(
                id=r.id,
                cliente_id=r.cliente_id,
                titulo=r.titulo,
                descripcion=r.descripcion,
                comidas=r.comidas,
                fecha_asignacion=r.fecha_asignacion,
                activa=r.activa
            ) for r in resultados
        ]
    
    def obtener_activa_por_cliente(self, cliente_id: int) -> Optional[Dieta]:
        sql = text("""
            SELECT * FROM dietas 
            WHERE cliente_id = :cliente_id AND activa = 1
        """)
        result = self.session.execute(sql, {'cliente_id': cliente_id}).first()
        
        if not result:
            return None
        
        return Dieta(
            id=result.id,
            cliente_id=result.cliente_id,
            titulo=result.titulo,
            descripcion=result.descripcion,
            comidas=result.comidas,
            fecha_asignacion=result.fecha_asignacion,
            activa=result.activa
        )
    
    def listar_todas(self) -> List[Dieta]:
        sql = text("SELECT * FROM dietas ORDER BY fecha_asignacion DESC")
        resultados = self.session.execute(sql).fetchall()
        
        return [
            Dieta(
                id=r.id,
                cliente_id=r.cliente_id,
                titulo=r.titulo,
                descripcion=r.descripcion,
                comidas=r.comidas,
                fecha_asignacion=r.fecha_asignacion,
                activa=r.activa
            ) for r in resultados
        ]
    
    def eliminar(self, id: int) -> bool:
        sql = text("DELETE FROM dietas WHERE id = :id")
        result = self.session.execute(sql, {'id': id})
        self.session.commit()
        return result.rowcount > 0