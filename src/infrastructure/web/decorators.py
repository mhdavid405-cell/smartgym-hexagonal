from functools import wraps
from flask import session, redirect, request, jsonify

def login_requerido(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            # Si es API, devolver JSON, si es página, redirigir
            if request.path.startswith('/api/'):
                return jsonify({'error': 'No autenticado'}), 401
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def rol_requerido(roles_permitidos):
    """Decorador para rutas que requieren un rol específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'usuario_id' not in session:
                if request.path.startswith('/api/'):
                    return jsonify({'error': 'No autenticado'}), 401
                return redirect('/login')
            
            rol_usuario = session.get('usuario_rol')
            if rol_usuario not in roles_permitidos:
                if request.path.startswith('/api/'):
                    return jsonify({'error': 'No autorizado'}), 403
                return redirect('/')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_requerido(f):
    """Decorador para rutas solo de administrador"""
    return rol_requerido(['admin'])(f)

def entrenador_requerido(f):
    """Decorador para rutas de administrador y entrenador"""
    return rol_requerido(['admin', 'entrenador'])(f)

def cliente_requerido(f):
    """Decorador para rutas accesibles por todos los autenticados"""
    return login_requerido(f)