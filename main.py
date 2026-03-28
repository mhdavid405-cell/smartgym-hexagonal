from flask import Flask, render_template, session
import os
from src.infrastructure.web.controllers.cliente_controller import cliente_bp
from src.infrastructure.web.controllers.membresia_controller import membresia_bp
from src.infrastructure.web.controllers.rutina_controller import rutina_bp
from src.infrastructure.web.controllers.dieta_controller import dieta_bp
from src.infrastructure.web.controllers.progreso_controller import progreso_bp
from src.infrastructure.web.controllers.auth_controller import auth_bp
from src.infrastructure.web.decorators import login_requerido, admin_requerido, entrenador_requerido

def create_app():
    app = Flask(__name__,
                template_folder='src/infrastructure/web/templates',
                static_folder='src/infrastructure/web/static')
    
    # Configuración de sesión
    app.secret_key = os.getenv('SECRET_KEY', 'mi-clave-secreta-para-sesiones')
    
    # Registrar blueprints de API
    app.register_blueprint(cliente_bp)
    app.register_blueprint(membresia_bp)
    app.register_blueprint(rutina_bp)
    app.register_blueprint(dieta_bp)
    app.register_blueprint(progreso_bp)
    app.register_blueprint(auth_bp)

    # ========== RUTAS PÚBLICAS ==========
    @app.route('/')
    def landing():
        return render_template('landing.html')
    
    @app.route('/login')
    def login_page():
        return render_template('login.html')
    
    @app.route('/membresias')
    def lista_membresias():
        return render_template('membresias.html')
    
    # ========== RUTAS DE DASHBOARDS POR ROL ==========
    @app.route('/dashboard')
    @login_requerido
    def dashboard():
        """Redirige al dashboard según el rol del usuario"""
        rol = session.get('usuario_rol')
        if rol == 'admin':
            return render_template('admin/dashboard.html')
        elif rol == 'entrenador':
            return render_template('entrenador/dashboard.html')
        else:
            return render_template('cliente/dashboard.html')
    
    @app.route('/admin')
    @admin_requerido
    def admin_panel():
        return render_template('admin/dashboard.html')
    
    @app.route('/entrenador')
    @entrenador_requerido
    def entrenador_panel():
        return render_template('entrenador/dashboard.html')
    
    # ========== RUTAS PROTEGIDAS (TODOS LOS AUTENTICADOS) ==========
    @app.route('/clientes')
    @login_requerido
    def lista_clientes():
        return render_template('clientes.html')
    
    @app.route('/clientes/nuevo')
    @login_requerido
    def nuevo_cliente():
        return render_template('nuevo_cliente.html')
    
    @app.route('/clientes/<int:id>')
    @login_requerido
    def detalle_cliente(id):
        return render_template('detalle_cliente.html')
    
    @app.route('/clientes/<int:id>/editar')
    @login_requerido
    def editar_cliente(id):
        return render_template('editar_cliente.html')
    
    # ========== RUTAS DE RUTINAS (ENTRENADOR Y ADMIN) ==========
    @app.route('/rutinas')
    @entrenador_requerido
    def lista_rutinas():
        return render_template('rutinas.html')
    
    @app.route('/rutinas/nueva')
    @entrenador_requerido
    def nueva_rutina():
        return render_template('nueva_rutina.html')
    
    @app.route('/rutinas/<int:id>')
    @entrenador_requerido
    def detalle_rutina(id):
        return render_template('detalle_rutina.html')
    
    @app.route('/rutinas/<int:id>/editar')
    @entrenador_requerido
    def editar_rutina(id):
        return render_template('editar_rutina.html')
    
    # ========== RUTAS DE DIETAS (ENTRENADOR Y ADMIN) ==========
    @app.route('/dietas')
    @entrenador_requerido
    def lista_dietas():
        return render_template('dietas.html')
    
    @app.route('/dietas/nueva')
    @entrenador_requerido
    def nueva_dieta():
        return render_template('nueva_dieta.html')
    
    @app.route('/dietas/<int:id>')
    @entrenador_requerido
    def detalle_dieta(id):
        return render_template('detalle_dieta.html')
    
    @app.route('/dietas/<int:id>/editar')
    @entrenador_requerido
    def editar_dieta(id):
        return render_template('editar_dieta.html')
    
    # ========== RUTAS DE PROGRESO (ENTRENADOR Y ADMIN) ==========
    @app.route('/progreso')
    @entrenador_requerido
    def lista_progreso():
        return render_template('progreso.html')

    @app.route('/progreso/nuevo')
    @entrenador_requerido
    def nuevo_progreso():
        return render_template('nuevo_progreso.html')

    @app.route('/progreso/cliente/<int:cliente_id>')
    @entrenador_requerido
    def historial_progreso(cliente_id):
        return render_template('historial_progreso.html')

    @app.route('/progreso/<int:id>/editar')
    @entrenador_requerido
    def editar_progreso_view(id):
        return render_template('editar_progreso.html')
    
    # ========== RUTAS DE ADMINISTRACIÓN ==========
    @app.route('/usuarios')
    @admin_requerido
    def lista_usuarios():
        return render_template('admin/usuarios.html')
    
    @app.route('/reportes')
    @admin_requerido
    def reportes():
        return render_template('admin/reportes.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)