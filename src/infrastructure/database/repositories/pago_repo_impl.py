from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.domain.entities.pago import Pago
from src.domain.interfaces.repositorios.pago_repositorio import PagoRepositorio

class PagoRepositorioSQLServer(PagoRepositorio):
    def __init__(self, session: Session):
        self.session = session
    
    def guardar(self, pago: Pago) -> Pago:
        """Guarda un pago usando SQL directo"""
        
        if pago.id:
            # Actualizar
            sql = text("""
                UPDATE pagos 
                SET monto = :monto, 
                    metodo_pago = :metodo_pago,
                    estado = :estado
                WHERE id = :id
            """)
            self.session.execute(sql, {
                'id': pago.id,
                'monto': pago.monto,
                'metodo_pago': pago.metodo_pago,
                'estado': pago.estado
            })
        else:
            # Insertar nuevo
            sql = text("""
                INSERT INTO pagos (cliente_id, membresia_id, monto, fecha_pago, fecha_vencimiento, metodo_pago, estado)
                OUTPUT INSERTED.id
                VALUES (:cliente_id, :membresia_id, :monto, :fecha_pago, :fecha_vencimiento, :metodo_pago, :estado)
            """)
            result = self.session.execute(sql, {
                'cliente_id': pago.cliente_id,
                'membresia_id': pago.membresia_id,
                'monto': pago.monto,
                'fecha_pago': pago.fecha_pago,
                'fecha_vencimiento': pago.fecha_vencimiento,
                'metodo_pago': pago.metodo_pago,
                'estado': pago.estado
            })
            pago.id = result.fetchone()[0]
        
        self.session.commit()
        return pago
    
    def obtener_por_id(self, id: int) -> Optional[Pago]:
        sql = text("SELECT * FROM pagos WHERE id = :id")
        result = self.session.execute(sql, {'id': id}).first()
        
        if not result:
            return None
        
        return Pago(
            id=result.id,
            cliente_id=result.cliente_id,
            membresia_id=result.membresia_id,
            monto=result.monto,
            fecha_pago=result.fecha_pago,
            fecha_vencimiento=result.fecha_vencimiento,
            metodo_pago=result.metodo_pago,
            estado=result.estado
        )
    
    def obtener_por_cliente(self, cliente_id: int) -> List[Pago]:
        sql = text("""
            SELECT * FROM pagos 
            WHERE cliente_id = :cliente_id 
            ORDER BY fecha_pago DESC
        """)
        resultados = self.session.execute(sql, {'cliente_id': cliente_id}).fetchall()
        
        return [
            Pago(
                id=r.id,
                cliente_id=r.cliente_id,
                membresia_id=r.membresia_id,
                monto=r.monto,
                fecha_pago=r.fecha_pago,
                fecha_vencimiento=r.fecha_vencimiento,
                metodo_pago=r.metodo_pago,
                estado=r.estado
            ) for r in resultados
        ]
    
    def listar_todos(self) -> List[Pago]:
        sql = text("SELECT * FROM pagos ORDER BY fecha_pago DESC")
        resultados = self.session.execute(sql).fetchall()
        
        return [
            Pago(
                id=r.id,
                cliente_id=r.cliente_id,
                membresia_id=r.membresia_id,
                monto=r.monto,
                fecha_pago=r.fecha_pago,
                fecha_vencimiento=r.fecha_vencimiento,
                metodo_pago=r.metodo_pago,
                estado=r.estado
            ) for r in resultados
        ]
    
    def obtener_pagos_por_rango(self, fecha_inicio, fecha_fin) -> List[Pago]:
        sql = text("""
            SELECT * FROM pagos 
            WHERE fecha_pago BETWEEN :inicio AND :fin
            ORDER BY fecha_pago DESC
        """)
        resultados = self.session.execute(sql, {
            'inicio': fecha_inicio,
            'fin': fecha_fin
        }).fetchall()
        
        return [
            Pago(
                id=r.id,
                cliente_id=r.cliente_id,
                membresia_id=r.membresia_id,
                monto=r.monto,
                fecha_pago=r.fecha_pago,
                fecha_vencimiento=r.fecha_vencimiento,
                metodo_pago=r.metodo_pago,
                estado=r.estado
            ) for r in resultados
        ]
    
    def obtener_total_ingresos_por_mes(self, año: int, mes: int) -> float:
        sql = text("""
            SELECT COALESCE(SUM(monto), 0) as total
            FROM pagos 
            WHERE YEAR(fecha_pago) = :año 
            AND MONTH(fecha_pago) = :mes
            AND estado = 'COMPLETADO'
        """)
        result = self.session.execute(sql, {'año': año, 'mes': mes}).first()
        return float(result[0]) if result else 0.0