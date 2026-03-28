from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class RolUsuario(Enum):
    ADMIN = "admin"
    ENTRENADOR = "entrenador"
    CLIENTE = "cliente"

@dataclass
class Usuario:
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    rol: RolUsuario = RolUsuario.CLIENTE
    cliente_id: Optional[int] = None
    activo: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def verificar_password(self, password: str, bcrypt) -> bool:
        """Verifica si la contraseña es correcta"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def es_admin(self) -> bool:
        return self.rol == RolUsuario.ADMIN
    
    def es_entrenador(self) -> bool:
        return self.rol == RolUsuario.ENTRENADOR
    
    def es_cliente(self) -> bool:
        return self.rol == RolUsuario.CLIENTE
    
    def tiene_permiso(self, rol_requerido: str) -> bool:
        """Verifica si el usuario tiene el rol requerido"""
        return self.rol.value == rol_requerido