import bcrypt
from typing import Optional
from src.domain.entities.usuario import Usuario, RolUsuario
from src.domain.interfaces.repositorios.usuario_repositorio import UsuarioRepositorio

class AutenticarUsuario:
    """
    Caso de uso: Autenticación de usuarios.
    
    Responsabilidades:
    - Registrar nuevos usuarios
    - Iniciar sesión (validar credenciales)
    - Cambiar contraseña
    - Obtener usuario por ID
    """
    
    def __init__(self, usuario_repo: UsuarioRepositorio):
        self.usuario_repo = usuario_repo
    
    def registrar(self, username: str, email: str, password: str, 
                  rol: str = 'cliente', cliente_id: int = None) -> Usuario:
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            username: Nombre de usuario
            email: Correo electrónico
            password: Contraseña en texto plano
            rol: Rol del usuario (admin, entrenador, cliente)
            cliente_id: ID del cliente asociado (si aplica)
        
        Returns:
            Usuario: El usuario creado
            
        Raises:
            ValueError: Si el username o email ya existen
        """
        # Verificar que username no exista
        existente = self.usuario_repo.obtener_por_username(username)
        if existente:
            raise ValueError(f"El nombre de usuario '{username}' ya está en uso")
        
        # Verificar que email no exista
        existente_email = self.usuario_repo.obtener_por_email(email)
        if existente_email:
            raise ValueError(f"El email '{email}' ya está registrado")
        
        # Hashear contraseña
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        # Crear usuario
        usuario = Usuario(
            id=None,
            username=username,
            email=email,
            password_hash=password_hash,
            rol=RolUsuario(rol),
            cliente_id=cliente_id,
            activo=True
        )
        
        return self.usuario_repo.guardar(usuario)
    
    def login(self, username: str, password: str) -> Optional[Usuario]:
        """
        Inicia sesión de un usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
        
        Returns:
            Optional[Usuario]: El usuario si las credenciales son correctas, None si no
        
        Raises:
            ValueError: Si el usuario está inactivo
        """
        usuario = self.usuario_repo.obtener_por_username(username)
        
        if not usuario:
            return None
        
        if not usuario.activo:
            raise ValueError("Usuario inactivo, contacta al administrador")
        
        # Verificar contraseña
        if bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
            return usuario
        
        return None
    
    def obtener_usuario_por_id(self, id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        return self.usuario_repo.obtener_por_id(id)
    
    def cambiar_contraseña(self, id: int, nueva_password: str) -> bool:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            id: ID del usuario
            nueva_password: Nueva contraseña en texto plano
        
        Returns:
            bool: True si se actualizó correctamente
            
        Raises:
            ValueError: Si el usuario no existe
        """
        usuario = self.usuario_repo.obtener_por_id(id)
        if not usuario:
            raise ValueError(f"Usuario {id} no encontrado")
        
        # Hashear nueva contraseña
        salt = bcrypt.gensalt()
        usuario.password_hash = bcrypt.hashpw(nueva_password.encode('utf-8'), salt).decode('utf-8')
        
        self.usuario_repo.guardar(usuario)
        return True