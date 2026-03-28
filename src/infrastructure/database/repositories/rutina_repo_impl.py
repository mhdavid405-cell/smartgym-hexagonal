from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.domain.entities.rutina import Rutina
from src.domain.interfaces.repositorios.rutina_repositorio import RutinaRepositorio

class RutinaRepositorioSQLServer(RutinaRepositorio):
    def __init__(self, session: Session):
        self.session = session
    
    def guardar(self, rutina: Rutina) -> Rutina:
        """Guarda una rutina usando SQL directo para evitar problemas de mapeo"""
        
        if rutina.id:
            # Actualizar
            sql = text("""
                UPDATE rutinas 
                SET titulo = :titulo, 
                    descripcion = :descripcion, 
                    ejercicios = :ejercicios,
                    activa = :activa
                WHERE id = :id
            """)
            self.session.execute(sql, {
                'id': rutina.id,
                'titulo': rutina.titulo,
                'descripcion': rutina.descripcion,
                'ejercicios': rutina.ejercicios,
                'activa': rutina.activa
            })
        else:
            # Insertar nuevo
            sql = text("""
                INSERT INTO rutinas (cliente_id, titulo, descripcion, ejercicios, fecha_asignacion, activa)
                OUTPUT INSERTED.id
                VALUES (:cliente_id, :titulo, :descripcion, :ejercicios, :fecha_asignacion, :activa)
            """)
            result = self.session.execute(sql, {
                'cliente_id': rutina.cliente_id,
                'titulo': rutina.titulo,
                'descripcion': rutina.descripcion,
                'ejercicios': rutina.ejercicios,
                'fecha_asignacion': rutina.fecha_asignacion,
                'activa': rutina.activa
            })
            rutina.id = result.fetchone()[0]
        
        self.session.commit()
        return rutina
    
    def obtener_por_id(self, id: int) -> Optional[Rutina]:
        sql = text("SELECT * FROM rutinas WHERE id = :id")
        result = self.session.execute(sql, {'id': id}).first()
        
        if not result:
            return None
        
        return Rutina(
            id=result.id,
            cliente_id=result.cliente_id,
            titulo=result.titulo,
            descripcion=result.descripcion,
            ejercicios=result.ejercicios,
            fecha_asignacion=result.fecha_asignacion,
            activa=result.activa
        )
    
    def obtener_por_cliente(self, cliente_id: int) -> List[Rutina]:
        sql = text("""
            SELECT * FROM rutinas 
            WHERE cliente_id = :cliente_id 
            ORDER BY fecha_asignacion DESC
        """)
        resultados = self.session.execute(sql, {'cliente_id': cliente_id}).fetchall()
        
        return [
            Rutina(
                id=r.id,
                cliente_id=r.cliente_id,
                titulo=r.titulo,
                descripcion=r.descripcion,
                ejercicios=r.ejercicios,
                fecha_asignacion=r.fecha_asignacion,
                activa=r.activa
            ) for r in resultados
        ]
    
    def obtener_activa_por_cliente(self, cliente_id: int) -> Optional[Rutina]:
        sql = text("""
            SELECT * FROM rutinas 
            WHERE cliente_id = :cliente_id AND activa = 1
        """)
        result = self.session.execute(sql, {'cliente_id': cliente_id}).first()
        
        if not result:
            return None
        
        return Rutina(
            id=result.id,
            cliente_id=result.cliente_id,
            titulo=result.titulo,
            descripcion=result.descripcion,
            ejercicios=result.ejercicios,
            fecha_asignacion=result.fecha_asignacion,
            activa=result.activa
        )
    
    def listar_todas(self) -> List[Rutina]:
        sql = text("SELECT * FROM rutinas ORDER BY fecha_asignacion DESC")
        resultados = self.session.execute(sql).fetchall()
        
        return [
            Rutina(
                id=r.id,
                cliente_id=r.cliente_id,
                titulo=r.titulo,
                descripcion=r.descripcion,
                ejercicios=r.ejercicios,
                fecha_asignacion=r.fecha_asignacion,
                activa=r.activa
            ) for r in resultados
        ]
    
    def eliminar(self, id: int) -> bool:
        sql = text("DELETE FROM rutinas WHERE id = :id")
        result = self.session.execute(sql, {'id': id})
        self.session.commit()
        return result.rowcount > 0