from flask import Blueprint, request, jsonify
from src.config.database import DatabaseConfig
from src.infrastructure.database.repositories.rutina_repo_impl import RutinaRepositorioSQLServer
from src.infrastructure.database.repositories.cliente_repo_impl import ClienteRepositorioSQLServer
from src.domain.use_cases.gestionar_rutina import GestionarRutina
from src.domain.entities.rutina import Rutina

# Crear blueprint para rutinas
rutina_bp = Blueprint('rutinas', __name__, url_prefix='/api/rutinas')

def get_gestionar_rutina():
    """Factory function para obtener el caso de uso de rutinas"""
    db_config = DatabaseConfig()
    session = db_config.get_session()
    rutina_repo = RutinaRepositorioSQLServer(session)
    cliente_repo = ClienteRepositorioSQLServer(session)
    return GestionarRutina(rutina_repo, cliente_repo), session

# ========== LISTAR TODAS LAS RUTINAS ==========
@rutina_bp.route('', methods=['GET'])
def listar_rutinas():
    """GET /api/rutinas - Listar todas las rutinas"""
    caso_uso, session = get_gestionar_rutina()
    try:
        rutinas = caso_uso.listar_todas()
        
        return jsonify([{
            'id': r.id,
            'cliente_id': r.cliente_id,
            'titulo': r.titulo,
            'descripcion': r.descripcion,
            'ejercicios': r.ejercicios,
            'fecha_asignacion': r.fecha_asignacion.isoformat(),
            'activa': r.activa
        } for r in rutinas])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== CREAR NUEVA RUTINA ==========
@rutina_bp.route('', methods=['POST'])
def asignar_rutina():
    """POST /api/rutinas - Asignar nueva rutina a un cliente"""
    caso_uso, session = get_gestionar_rutina()
    try:
        data = request.get_json()
        
        rutina = caso_uso.asignar_rutina(
            cliente_id=data['cliente_id'],
            titulo=data['titulo'],
            descripcion=data.get('descripcion', ''),
            ejercicios=data['ejercicios']
        )
        
        return jsonify({
            'id': rutina.id,
            'mensaje': 'Rutina asignada exitosamente',
            'cliente_id': rutina.cliente_id,
            'titulo': rutina.titulo,
            'fecha_asignacion': rutina.fecha_asignacion.isoformat()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== ACTUALIZAR RUTINA ==========
@rutina_bp.route('/<int:id>', methods=['PUT'])
def actualizar_rutina(id):
    """PUT /api/rutinas/{id} - Actualizar una rutina existente"""
    caso_uso, session = get_gestionar_rutina()
    try:
        data = request.get_json()
        
        # Obtener la rutina existente
        rutina_existente = caso_uso.obtener_rutina(id)
        if not rutina_existente:
            return jsonify({'error': 'Rutina no encontrada'}), 404
        
        # Crear rutina actualizada
        rutina_actualizada = Rutina(
            id=id,
            cliente_id=data.get('cliente_id', rutina_existente.cliente_id),
            titulo=data.get('titulo', rutina_existente.titulo),
            descripcion=data.get('descripcion', rutina_existente.descripcion),
            ejercicios=data.get('ejercicios', rutina_existente.ejercicios),
            fecha_asignacion=rutina_existente.fecha_asignacion,
            activa=data.get('activa', rutina_existente.activa)
        )
        
        # Guardar cambios
        resultado = caso_uso.rutina_repo.guardar(rutina_actualizada)
        
        return jsonify({
            'id': resultado.id,
            'mensaje': 'Rutina actualizada exitosamente'
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== RUTINAS POR CLIENTE ==========
@rutina_bp.route('/cliente/<int:cliente_id>', methods=['GET'])
def rutinas_por_cliente(cliente_id):
    """GET /api/rutinas/cliente/{cliente_id} - Historial de rutinas de un cliente"""
    caso_uso, session = get_gestionar_rutina()
    try:
        rutinas = caso_uso.obtener_rutinas_cliente(cliente_id)
        
        return jsonify([{
            'id': r.id,
            'cliente_id': r.cliente_id,
            'titulo': r.titulo,
            'descripcion': r.descripcion,
            'ejercicios': r.ejercicios,
            'fecha_asignacion': r.fecha_asignacion.isoformat(),
            'activa': r.activa
        } for r in rutinas])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== RUTINA ACTIVA DEL CLIENTE ==========
@rutina_bp.route('/cliente/<int:cliente_id>/activa', methods=['GET'])
def rutina_activa(cliente_id):
    """GET /api/rutinas/cliente/{cliente_id}/activa - Obtener rutina activa de un cliente"""
    caso_uso, session = get_gestionar_rutina()
    try:
        rutina = caso_uso.obtener_rutina_activa(cliente_id)
        
        if not rutina:
            return jsonify({'mensaje': 'El cliente no tiene rutina activa'}), 404
        
        return jsonify({
            'id': rutina.id,
            'cliente_id': rutina.cliente_id,
            'titulo': rutina.titulo,
            'descripcion': rutina.descripcion,
            'ejercicios': rutina.ejercicios,
            'fecha_asignacion': rutina.fecha_asignacion.isoformat(),
            'activa': rutina.activa
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== OBTENER RUTINA POR ID ==========
@rutina_bp.route('/<int:id>', methods=['GET'])
def obtener_rutina(id):
    """GET /api/rutinas/{id} - Obtener rutina por ID"""
    caso_uso, session = get_gestionar_rutina()
    try:
        rutina = caso_uso.obtener_rutina(id)
        
        if not rutina:
            return jsonify({'error': 'Rutina no encontrada'}), 404
        
        return jsonify({
            'id': rutina.id,
            'cliente_id': rutina.cliente_id,
            'titulo': rutina.titulo,
            'descripcion': rutina.descripcion,
            'ejercicios': rutina.ejercicios,
            'fecha_asignacion': rutina.fecha_asignacion.isoformat(),
            'activa': rutina.activa
        })
        
    finally:
        session.close()

# ========== DESACTIVAR RUTINA ==========
@rutina_bp.route('/<int:id>/desactivar', methods=['PUT'])
def desactivar_rutina(id):
    """PUT /api/rutinas/{id}/desactivar - Desactivar una rutina"""
    caso_uso, session = get_gestionar_rutina()
    try:
        caso_uso.desactivar_rutina(id)
        return jsonify({'mensaje': 'Rutina desactivada exitosamente'})
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    finally:
        session.close()

# ========== ELIMINAR RUTINA ==========
@rutina_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_rutina(id):
    """DELETE /api/rutinas/{id} - Eliminar una rutina"""
    caso_uso, session = get_gestionar_rutina()
    try:
        resultado = caso_uso.eliminar_rutina(id)
        if resultado:
            return jsonify({'mensaje': 'Rutina eliminada exitosamente'})
        return jsonify({'error': 'Rutina no encontrada'}), 404
        
    finally:
        session.close()