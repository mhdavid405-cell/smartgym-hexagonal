from flask import Blueprint, request, jsonify
from src.config.database import DatabaseConfig
from src.infrastructure.database.repositories.progreso_repo_impl import ProgresoRepositorioSQLServer
from src.infrastructure.database.repositories.cliente_repo_impl import ClienteRepositorioSQLServer
from src.domain.use_cases.gestionar_progreso import GestionarProgreso
from src.domain.entities.progreso import Progreso
from datetime import date

# Crear blueprint para progreso
progreso_bp = Blueprint('progreso', __name__, url_prefix='/api/progreso')

def get_gestionar_progreso():
    """Factory function para obtener el caso de uso de progreso"""
    db_config = DatabaseConfig()
    session = db_config.get_session()
    progreso_repo = ProgresoRepositorioSQLServer(session)
    cliente_repo = ClienteRepositorioSQLServer(session)
    return GestionarProgreso(progreso_repo, cliente_repo), session

# ========== LISTAR TODOS LOS REGISTROS ==========
@progreso_bp.route('', methods=['GET'])
def listar_progreso():
    """GET /api/progreso - Listar todos los registros de progreso"""
    caso_uso, session = get_gestionar_progreso()
    try:
        registros = caso_uso.listar_todos()
        
        return jsonify([{
            'id': r.id,
            'cliente_id': r.cliente_id,
            'fecha': r.fecha.isoformat(),
            'peso': r.peso,
            'altura': r.altura,
            'brazos': r.brazos,
            'pecho': r.pecho,
            'cintura': r.cintura,
            'piernas': r.piernas,
            'notas': r.notas
        } for r in registros])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== REGISTRAR NUEVAS MEDIDAS ==========
@progreso_bp.route('', methods=['POST'])
def registrar_medidas():
    """POST /api/progreso - Registrar nuevas medidas de un cliente"""
    caso_uso, session = get_gestionar_progreso()
    try:
        data = request.get_json()
        
        progreso = caso_uso.registrar_medidas(
            cliente_id=data['cliente_id'],
            peso=data.get('peso'),
            altura=data.get('altura'),
            brazos=data.get('brazos'),
            pecho=data.get('pecho'),
            cintura=data.get('cintura'),
            piernas=data.get('piernas'),
            notas=data.get('notas')
        )
        
        return jsonify({
            'id': progreso.id,
            'mensaje': 'Medidas registradas exitosamente',
            'cliente_id': progreso.cliente_id,
            'fecha': progreso.fecha.isoformat()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== ACTUALIZAR REGISTRO DE PROGRESO ==========
@progreso_bp.route('/<int:id>', methods=['PUT'])
def actualizar_progreso(id):
    """PUT /api/progreso/{id} - Actualizar un registro de progreso existente"""
    caso_uso, session = get_gestionar_progreso()
    try:
        data = request.get_json()
        
        # Obtener registro existente
        registro_existente = caso_uso.obtener_progreso(id)
        if not registro_existente:
            return jsonify({'error': 'Registro no encontrado'}), 404
        
        # Crear registro actualizado
        progreso_actualizado = Progreso(
            id=id,
            cliente_id=data.get('cliente_id', registro_existente.cliente_id),
            fecha=data.get('fecha', registro_existente.fecha),
            peso=data.get('peso', registro_existente.peso),
            altura=data.get('altura', registro_existente.altura),
            brazos=data.get('brazos', registro_existente.brazos),
            pecho=data.get('pecho', registro_existente.pecho),
            cintura=data.get('cintura', registro_existente.cintura),
            piernas=data.get('piernas', registro_existente.piernas),
            notas=data.get('notas', registro_existente.notas)
        )
        
        # Guardar cambios
        resultado = caso_uso.progreso_repo.guardar(progreso_actualizado)
        
        return jsonify({
            'id': resultado.id,
            'mensaje': 'Registro actualizado exitosamente'
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== HISTORIAL POR CLIENTE ==========
@progreso_bp.route('/cliente/<int:cliente_id>', methods=['GET'])
def historial_cliente(cliente_id):
    """GET /api/progreso/cliente/{cliente_id} - Historial completo de un cliente"""
    caso_uso, session = get_gestionar_progreso()
    try:
        historial = caso_uso.obtener_historial_cliente(cliente_id)
        
        return jsonify([{
            'id': h.id,
            'cliente_id': h.cliente_id,
            'fecha': h.fecha.isoformat(),
            'peso': h.peso,
            'altura': h.altura,
            'brazos': h.brazos,
            'pecho': h.pecho,
            'cintura': h.cintura,
            'piernas': h.piernas,
            'notas': h.notas
        } for h in historial])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== ÚLTIMO REGISTRO DEL CLIENTE ==========
@progreso_bp.route('/cliente/<int:cliente_id>/ultimo', methods=['GET'])
def ultimo_registro(cliente_id):
    """GET /api/progreso/cliente/{cliente_id}/ultimo - Último registro del cliente"""
    caso_uso, session = get_gestionar_progreso()
    try:
        progreso = caso_uso.obtener_ultimo_registro(cliente_id)
        
        if not progreso:
            return jsonify({'mensaje': 'El cliente no tiene registros'}), 404
        
        return jsonify({
            'id': progreso.id,
            'cliente_id': progreso.cliente_id,
            'fecha': progreso.fecha.isoformat(),
            'peso': progreso.peso,
            'altura': progreso.altura,
            'brazos': progreso.brazos,
            'pecho': progreso.pecho,
            'cintura': progreso.cintura,
            'piernas': progreso.piernas,
            'notas': progreso.notas
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== EVOLUCIÓN DEL CLIENTE ==========
@progreso_bp.route('/cliente/<int:cliente_id>/evolucion', methods=['GET'])
def evolucion_cliente(cliente_id):
    """GET /api/progreso/cliente/{cliente_id}/evolucion - Calcular evolución del cliente"""
    caso_uso, session = get_gestionar_progreso()
    try:
        evolucion = caso_uso.calcular_evolucion(cliente_id)
        return jsonify(evolucion)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== OBTENER REGISTRO POR ID ==========
@progreso_bp.route('/<int:id>', methods=['GET'])
def obtener_registro(id):
    """GET /api/progreso/{id} - Obtener registro por ID"""
    caso_uso, session = get_gestionar_progreso()
    try:
        progreso = caso_uso.obtener_progreso(id)
        
        if not progreso:
            return jsonify({'error': 'Registro no encontrado'}), 404
        
        return jsonify({
            'id': progreso.id,
            'cliente_id': progreso.cliente_id,
            'fecha': progreso.fecha.isoformat(),
            'peso': progreso.peso,
            'altura': progreso.altura,
            'brazos': progreso.brazos,
            'pecho': progreso.pecho,
            'cintura': progreso.cintura,
            'piernas': progreso.piernas,
            'notas': progreso.notas
        })
        
    finally:
        session.close()

# ========== ELIMINAR REGISTRO ==========
@progreso_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_registro(id):
    """DELETE /api/progreso/{id} - Eliminar un registro"""
    caso_uso, session = get_gestionar_progreso()
    try:
        resultado = caso_uso.eliminar_registro(id)
        if resultado:
            return jsonify({'mensaje': 'Registro eliminado exitosamente'})
        return jsonify({'error': 'Registro no encontrado'}), 404
        
    finally:
        session.close()