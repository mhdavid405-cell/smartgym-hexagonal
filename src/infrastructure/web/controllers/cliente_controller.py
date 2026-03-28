from flask import Blueprint, request, jsonify
from src.config.database import DatabaseConfig
from src.infrastructure.database.repositories.cliente_repo_impl import ClienteRepositorioSQLServer
from src.domain.use_cases.gestionar_cliente import GestionarCliente
from src.domain.entities.cliente import Cliente
from datetime import date
from sqlalchemy import text

# Crear blueprint para clientes
cliente_bp = Blueprint('clientes', __name__, url_prefix='/api/clientes')

def get_gestionar_cliente():
    """Factory function para obtener el caso de uso con su repositorio"""
    db_config = DatabaseConfig()
    session = db_config.get_session()
    repo = ClienteRepositorioSQLServer(session)
    return GestionarCliente(repo), session

@cliente_bp.route('', methods=['GET'])
def listar_clientes():
    """GET /api/clientes?activos=true"""
    caso_uso, session = get_gestionar_cliente()
    try:
        solo_activos = request.args.get('activos', '').lower() == 'true'
        clientes = caso_uso.listar_clientes(solo_activos)
        
        result = []
        for c in clientes:
            cliente_dict = {
                'id': c.id,
                'nombre': c.nombre,
                'apellido': c.apellido,
                'dni': c.dni,
                'email': c.email,
                'telefono': c.telefono,
                'activo': c.activo,
                'fecha_registro': c.fecha_registro.isoformat() if c.fecha_registro else None,
                'membresia_id': c.membresia_id
            }
            
            # Obtener nombre de membresía si tiene
            if c.membresia_id:
                engine = session.get_bind()
                with engine.connect() as conn:
                    result_sql = conn.execute(
                        text("SELECT tipo FROM membresias WHERE id = :id"),
                        {"id": c.membresia_id}
                    ).first()
                    if result_sql:
                        cliente_dict['membresia_nombre'] = result_sql[0]
                    else:
                        cliente_dict['membresia_nombre'] = None
            else:
                cliente_dict['membresia_nombre'] = None
            
            result.append(cliente_dict)
        
        return jsonify(result)
    finally:
        session.close()

@cliente_bp.route('', methods=['POST'])
def crear_cliente():
    """POST /api/clientes"""
    caso_uso, session = get_gestionar_cliente()
    try:
        data = request.get_json()
        
        cliente = caso_uso.registrar_cliente(
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni'],
            email=data.get('email'),
            telefono=data.get('telefono')
        )
        
        return jsonify({
            'id': cliente.id,
            'mensaje': 'Cliente creado exitosamente'
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@cliente_bp.route('/<int:id>', methods=['GET'])
def obtener_cliente(id):
    """GET /api/clientes/{id}"""
    caso_uso, session = get_gestionar_cliente()
    try:
        cliente = caso_uso.obtener_cliente(id)
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        
        result = {
            'id': cliente.id,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'dni': cliente.dni,
            'email': cliente.email,
            'telefono': cliente.telefono,
            'activo': cliente.activo,
            'fecha_registro': cliente.fecha_registro.isoformat() if cliente.fecha_registro else None,
            'membresia_id': cliente.membresia_id
        }
        
        # Obtener nombre de membresía si tiene
        if cliente.membresia_id:
            engine = session.get_bind()
            with engine.connect() as conn:
                result_sql = conn.execute(
                    text("SELECT tipo FROM membresias WHERE id = :id"),
                    {"id": cliente.membresia_id}
                ).first()
                if result_sql:
                    result['membresia_nombre'] = result_sql[0]
                else:
                    result['membresia_nombre'] = None
        else:
            result['membresia_nombre'] = None
        
        return jsonify(result)
    finally:
        session.close()

@cliente_bp.route('/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    """PUT /api/clientes/{id} - Actualizar cliente existente"""
    caso_uso, session = get_gestionar_cliente()
    try:
        data = request.get_json()
        
        # Verificar que el cliente existe
        cliente_existente = caso_uso.obtener_cliente(id)
        if not cliente_existente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        
        # Log para depuración
        print(f"Datos recibidos en PUT: {data}")
        
        # Crear cliente actualizado (INCLUYENDO membresia_id)
        cliente_actualizado = Cliente(
            id=id,
            nombre=data['nombre'],
            apellido=data['apellido'],
            dni=data['dni'],
            email=data.get('email'),
            telefono=data.get('telefono'),
            fecha_registro=cliente_existente.fecha_registro,  # Mantener fecha original
            activo=data.get('activo', cliente_existente.activo),
            membresia_id=data.get('membresia_id')  # ← LÍNEA CLAVE PARA GUARDAR MEMBRESÍA
        )
        
        # Guardar cambios
        resultado = caso_uso.cliente_repo.guardar(cliente_actualizado)
        
        return jsonify({
            'id': resultado.id,
            'mensaje': 'Cliente actualizado exitosamente'
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@cliente_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    """DELETE /api/clientes/{id} (baja lógica)"""
    caso_uso, session = get_gestionar_cliente()
    try:
        caso_uso.dar_de_baja(id)
        return jsonify({'mensaje': 'Cliente desactivado exitosamente'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    finally:
        session.close()