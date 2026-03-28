from flask import Blueprint, request, jsonify
from src.config.database import DatabaseConfig
from src.infrastructure.database.repositories.pago_repo_impl import PagoRepositorioSQLServer
from src.infrastructure.database.repositories.cliente_repo_impl import ClienteRepositorioSQLServer
from src.infrastructure.database.repositories.membresia_repo_impl import MembresiaRepositorioSQLServer
from src.domain.use_cases.gestionar_pago import GestionarPago
from datetime import datetime

# Crear blueprint para pagos
pago_bp = Blueprint('pagos', __name__, url_prefix='/api/pagos')

def get_gestionar_pago():
    """Factory function para obtener el caso de uso de pagos"""
    db_config = DatabaseConfig()
    session = db_config.get_session()
    pago_repo = PagoRepositorioSQLServer(session)
    cliente_repo = ClienteRepositorioSQLServer(session)
    membresia_repo = MembresiaRepositorioSQLServer(session)
    return GestionarPago(pago_repo, cliente_repo, membresia_repo), session

@pago_bp.route('', methods=['POST'])
def registrar_pago():
    """POST /api/pagos - Registrar un nuevo pago"""
    caso_uso, session = get_gestionar_pago()
    try:
        data = request.get_json()
        
        pago = caso_uso.registrar_pago(
            cliente_id=data['cliente_id'],
            membresia_id=data['membresia_id'],
            monto=float(data['monto']),
            metodo_pago=data.get('metodo_pago', 'EFECTIVO')
        )
        
        return jsonify({
            'id': pago.id,
            'mensaje': 'Pago registrado exitosamente',
            'fecha_pago': pago.fecha_pago.isoformat(),
            'fecha_vencimiento': pago.fecha_vencimiento.isoformat()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@pago_bp.route('/cliente/<int:cliente_id>', methods=['GET'])
def pagos_por_cliente(cliente_id):
    """GET /api/pagos/cliente/{cliente_id} - Historial de pagos de un cliente"""
    caso_uso, session = get_gestionar_pago()
    try:
        pagos = caso_uso.obtener_pagos_cliente(cliente_id)
        
        return jsonify([{
            'id': p.id,
            'cliente_id': p.cliente_id,
            'membresia_id': p.membresia_id,
            'monto': p.monto,
            'fecha_pago': p.fecha_pago.isoformat(),
            'fecha_vencimiento': p.fecha_vencimiento.isoformat(),
            'metodo_pago': p.metodo_pago,
            'estado': p.estado
        } for p in pagos])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()