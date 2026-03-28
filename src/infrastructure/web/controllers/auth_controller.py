from flask import Blueprint, request, jsonify, session
from src.config.database import DatabaseConfig
from src.infrastructure.database.repositories.usuario_repo_impl import UsuarioRepositorioSQLServer
from src.domain.use_cases.autenticar_usuario import AutenticarUsuario

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def get_autenticar_usuario():
    db_config = DatabaseConfig()
    session_db = db_config.get_session()
    usuario_repo = UsuarioRepositorioSQLServer(session_db)
    return AutenticarUsuario(usuario_repo), session_db

# ========== REGISTRO ==========
@auth_bp.route('/registro', methods=['POST'])
def registrar():
    """POST /api/auth/registro - Registrar nuevo usuario"""
    caso_uso, session_db = get_autenticar_usuario()
    try:
        data = request.get_json()
        
        usuario = caso_uso.registrar(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            rol=data.get('rol', 'cliente'),
            cliente_id=data.get('cliente_id')
        )
        
        return jsonify({
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'rol': usuario.rol.value,
            'mensaje': 'Usuario registrado exitosamente'
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session_db.close()

# ========== LOGIN ==========
@auth_bp.route('/login', methods=['POST'])
def login():
    """POST /api/auth/login - Iniciar sesión"""
    caso_uso, session_db = get_autenticar_usuario()
    try:
        data = request.get_json()
        
        usuario = caso_uso.login(
            username=data['username'],
            password=data['password']
        )
        
        if usuario:
            # Guardar usuario en sesión
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.username
            session['usuario_rol'] = usuario.rol.value
            
            # Si es cliente, guardar cliente_id
            if usuario.cliente_id:
                session['usuario_cliente_id'] = usuario.cliente_id
            
            return jsonify({
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'rol': usuario.rol.value,
                'cliente_id': usuario.cliente_id,
                'mensaje': 'Login exitoso'
            }), 200
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
            
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session_db.close()

# ========== LOGOUT ==========
@auth_bp.route('/logout', methods=['POST'])
def logout():
    """POST /api/auth/logout - Cerrar sesión"""
    session.clear()
    return jsonify({'mensaje': 'Sesión cerrada exitosamente'}), 200

# ========== USUARIO ACTUAL ==========
@auth_bp.route('/usuario_actual', methods=['GET'])
def usuario_actual():
    """GET /api/auth/usuario_actual - Obtener usuario logueado"""
    if 'usuario_id' not in session:
        return jsonify({'error': 'No hay sesión activa'}), 401
    
    return jsonify({
        'id': session['usuario_id'],
        'username': session['usuario_nombre'],
        'rol': session['usuario_rol']
    }), 200

# ========== LISTAR USUARIOS (SOLO ADMIN) ==========
@auth_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """GET /api/usuarios - Listar todos los usuarios (solo admin)"""
    from flask import session
    
    # Verificar que sea admin
    if session.get('usuario_rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403
    
    caso_uso, session_db = get_autenticar_usuario()
    try:
        usuarios = caso_uso.usuario_repo.listar_todos()
        
        result = []
        for u in usuarios:
            usuario_dict = {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'rol': u.rol.value,
                'activo': u.activo,
                'cliente_id': u.cliente_id
            }
            
            # Obtener nombre del cliente asociado si existe
            if u.cliente_id:
                from sqlalchemy import text
                engine = session_db.get_bind()
                with engine.connect() as conn:
                    result_sql = conn.execute(
                        text("SELECT nombre, apellido FROM clientes WHERE id = :id"),
                        {"id": u.cliente_id}
                    ).first()
                    if result_sql:
                        usuario_dict['cliente_nombre'] = f"{result_sql[0]} {result_sql[1]}"
                    else:
                        usuario_dict['cliente_nombre'] = None
            else:
                usuario_dict['cliente_nombre'] = None
            
            result.append(usuario_dict)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session_db.close()

# ========== CREAR USUARIO (SOLO ADMIN) ==========
@auth_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    """POST /api/usuarios - Crear nuevo usuario (solo admin)"""
    from flask import session
    
    # Verificar que sea admin
    if session.get('usuario_rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403
    
    caso_uso, session_db = get_autenticar_usuario()
    try:
        data = request.get_json()
        
        usuario = caso_uso.registrar(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            rol=data.get('rol', 'cliente'),
            cliente_id=data.get('cliente_id')
        )
        
        return jsonify({
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'rol': usuario.rol.value,
            'mensaje': 'Usuario creado exitosamente'
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session_db.close()

# ========== ACTUALIZAR USUARIO (SOLO ADMIN) ==========
@auth_bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    """PUT /api/usuarios/{id} - Actualizar usuario (solo admin)"""
    from flask import session
    
    # Verificar que sea admin
    if session.get('usuario_rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403
    
    caso_uso, session_db = get_autenticar_usuario()
    try:
        data = request.get_json()
        
        usuario = caso_uso.usuario_repo.obtener_por_id(id)
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Actualizar campos
        usuario.username = data.get('username', usuario.username)
        usuario.email = data.get('email', usuario.email)
        usuario.rol = data.get('rol', usuario.rol)
        usuario.activo = data.get('activo', usuario.activo)
        
        if data.get('cliente_id') is not None:
            usuario.cliente_id = data.get('cliente_id')
        
        if data.get('password'):
            import bcrypt
            salt = bcrypt.gensalt()
            usuario.password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), salt).decode('utf-8')
        
        caso_uso.usuario_repo.guardar(usuario)
        
        return jsonify({
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'rol': usuario.rol.value,
            'mensaje': 'Usuario actualizado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session_db.close()

# ========== ELIMINAR USUARIO (SOLO ADMIN) ==========
@auth_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    """DELETE /api/usuarios/{id} - Eliminar usuario (solo admin)"""
    from flask import session
    
    # Verificar que sea admin
    if session.get('usuario_rol') != 'admin':
        return jsonify({'error': 'No autorizado'}), 403
    
    caso_uso, session_db = get_autenticar_usuario()
    try:
        resultado = caso_uso.usuario_repo.eliminar(id)
        if resultado:
            return jsonify({'mensaje': 'Usuario eliminado exitosamente'}), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session_db.close()