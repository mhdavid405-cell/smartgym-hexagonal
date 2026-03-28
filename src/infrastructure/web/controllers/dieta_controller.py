from flask import Blueprint, request, jsonify
from src.config.database import DatabaseConfig
from src.infrastructure.database.repositories.dieta_repo_impl import DietaRepositorioSQLServer
from src.infrastructure.database.repositories.cliente_repo_impl import ClienteRepositorioSQLServer
from src.domain.use_cases.gestionar_dieta import GestionarDieta
from src.domain.entities.dieta import Dieta

# Crear blueprint para dietas
dieta_bp = Blueprint('dietas', __name__, url_prefix='/api/dietas')

def get_gestionar_dieta():
    """Factory function para obtener el caso de uso de dietas"""
    db_config = DatabaseConfig()
    session = db_config.get_session()
    dieta_repo = DietaRepositorioSQLServer(session)
    cliente_repo = ClienteRepositorioSQLServer(session)
    return GestionarDieta(dieta_repo, cliente_repo), session

# ========== LISTAR TODAS LAS DIETAS ==========
@dieta_bp.route('', methods=['GET'])
def listar_dietas():
    """GET /api/dietas - Listar todas las dietas"""
    caso_uso, session = get_gestionar_dieta()
    try:
        dietas = caso_uso.listar_todas()
        
        return jsonify([{
            'id': d.id,
            'cliente_id': d.cliente_id,
            'titulo': d.titulo,
            'descripcion': d.descripcion,
            'comidas': d.comidas,
            'fecha_asignacion': d.fecha_asignacion.isoformat(),
            'activa': d.activa
        } for d in dietas])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== CREAR NUEVA DIETA ==========
@dieta_bp.route('', methods=['POST'])
def asignar_dieta():
    """POST /api/dietas - Asignar nueva dieta a un cliente"""
    caso_uso, session = get_gestionar_dieta()
    try:
        data = request.get_json()
        
        dieta = caso_uso.asignar_dieta(
            cliente_id=data['cliente_id'],
            titulo=data['titulo'],
            descripcion=data.get('descripcion', ''),
            comidas=data['comidas']
        )
        
        return jsonify({
            'id': dieta.id,
            'mensaje': 'Dieta asignada exitosamente',
            'cliente_id': dieta.cliente_id,
            'titulo': dieta.titulo,
            'fecha_asignacion': dieta.fecha_asignacion.isoformat()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== ACTUALIZAR DIETA ==========
@dieta_bp.route('/<int:id>', methods=['PUT'])
def actualizar_dieta(id):
    """PUT /api/dietas/{id} - Actualizar una dieta existente"""
    caso_uso, session = get_gestionar_dieta()
    try:
        data = request.get_json()
        
        # Obtener la dieta existente
        dieta_existente = caso_uso.obtener_dieta(id)
        if not dieta_existente:
            return jsonify({'error': 'Dieta no encontrada'}), 404
        
        # Crear dieta actualizada
        dieta_actualizada = Dieta(
            id=id,
            cliente_id=data.get('cliente_id', dieta_existente.cliente_id),
            titulo=data.get('titulo', dieta_existente.titulo),
            descripcion=data.get('descripcion', dieta_existente.descripcion),
            comidas=data.get('comidas', dieta_existente.comidas),
            fecha_asignacion=dieta_existente.fecha_asignacion,
            activa=data.get('activa', dieta_existente.activa)
        )
        
        # Guardar cambios
        resultado = caso_uso.dieta_repo.guardar(dieta_actualizada)
        
        return jsonify({
            'id': resultado.id,
            'mensaje': 'Dieta actualizada exitosamente'
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== DIETAS POR CLIENTE ==========
@dieta_bp.route('/cliente/<int:cliente_id>', methods=['GET'])
def dietas_por_cliente(cliente_id):
    """GET /api/dietas/cliente/{cliente_id} - Historial de dietas de un cliente"""
    caso_uso, session = get_gestionar_dieta()
    try:
        dietas = caso_uso.obtener_dietas_cliente(cliente_id)
        
        return jsonify([{
            'id': d.id,
            'cliente_id': d.cliente_id,
            'titulo': d.titulo,
            'descripcion': d.descripcion,
            'comidas': d.comidas,
            'fecha_asignacion': d.fecha_asignacion.isoformat(),
            'activa': d.activa
        } for d in dietas])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== DIETA ACTIVA DEL CLIENTE ==========
@dieta_bp.route('/cliente/<int:cliente_id>/activa', methods=['GET'])
def dieta_activa(cliente_id):
    """GET /api/dietas/cliente/{cliente_id}/activa - Obtener dieta activa de un cliente"""
    caso_uso, session = get_gestionar_dieta()
    try:
        dieta = caso_uso.obtener_dieta_activa(cliente_id)
        
        if not dieta:
            return jsonify({'mensaje': 'El cliente no tiene dieta activa'}), 404
        
        return jsonify({
            'id': dieta.id,
            'cliente_id': dieta.cliente_id,
            'titulo': dieta.titulo,
            'descripcion': dieta.descripcion,
            'comidas': dieta.comidas,
            'fecha_asignacion': dieta.fecha_asignacion.isoformat(),
            'activa': dieta.activa
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# ========== OBTENER DIETA POR ID ==========
@dieta_bp.route('/<int:id>', methods=['GET'])
def obtener_dieta(id):
    """GET /api/dietas/{id} - Obtener dieta por ID"""
    caso_uso, session = get_gestionar_dieta()
    try:
        dieta = caso_uso.obtener_dieta(id)
        
        if not dieta:
            return jsonify({'error': 'Dieta no encontrada'}), 404
        
        return jsonify({
            'id': dieta.id,
            'cliente_id': dieta.cliente_id,
            'titulo': dieta.titulo,
            'descripcion': dieta.descripcion,
            'comidas': dieta.comidas,
            'fecha_asignacion': dieta.fecha_asignacion.isoformat(),
            'activa': dieta.activa
        })
        
    finally:
        session.close()

# ========== DESACTIVAR DIETA ==========
@dieta_bp.route('/<int:id>/desactivar', methods=['PUT'])
def desactivar_dieta(id):
    """PUT /api/dietas/{id}/desactivar - Desactivar una dieta"""
    caso_uso, session = get_gestionar_dieta()
    try:
        caso_uso.desactivar_dieta(id)
        return jsonify({'mensaje': 'Dieta desactivada exitosamente'})
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    finally:
        session.close()

# ========== ELIMINAR DIETA ==========
@dieta_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_dieta(id):
    """DELETE /api/dietas/{id} - Eliminar una dieta"""
    caso_uso, session = get_gestionar_dieta()
    try:
        resultado = caso_uso.eliminar_dieta(id)
        if resultado:
            return jsonify({'mensaje': 'Dieta eliminada exitosamente'})
        return jsonify({'error': 'Dieta no encontrada'}), 404
        
    finally:
        session.close()