import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.database import DatabaseConfig
from src.infrastructure.database.repositories.cliente_repo_impl import ClienteRepositorioSQLServer
from src.domain.use_cases.gestionar_cliente import GestionarCliente
import random

print('🔍 Probando caso de uso: GestionarCliente')

try:
    db_config = DatabaseConfig()
    session = db_config.get_session()
    repo = ClienteRepositorioSQLServer(session)
    caso_uso = GestionarCliente(repo)
    
    # Usar un DNI aleatorio para evitar duplicados
    dni = f'{random.randint(10000000, 99999999)}'
    
    clientes = caso_uso.listar_clientes()
    print(f'✅ Clientes iniciales: {len(clientes)}')
    
    nuevo = caso_uso.registrar_cliente(
        nombre='Juan',
        apellido='Pérez',
        dni=dni,
        email='juan@email.com',
        telefono='555-1234'
    )
    print(f'✅ Cliente registrado: {nuevo.nombre} {nuevo.apellido} (ID: {nuevo.id}, DNI: {dni})')
    
    clientes = caso_uso.listar_clientes()
    print(f'✅ Clientes después de registrar: {len(clientes)}')
    
    obtenido = caso_uso.obtener_cliente(nuevo.id)
    print(f'✅ Cliente obtenido: {obtenido.nombre} {obtenido.apellido}')
    
    caso_uso.dar_de_baja(nuevo.id)
    print(f'✅ Cliente dado de baja')
    
    activos = caso_uso.listar_clientes(solo_activos=True)
    print(f'✅ Clientes activos: {len(activos)}')
    
    session.close()
    print('✅ Prueba de caso de uso exitosa')
    
except Exception as e:
    print(f'❌ Error: {e}')
