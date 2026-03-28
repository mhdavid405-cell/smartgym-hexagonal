import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.database import DatabaseConfig
from src.infrastructure.database.repositories.cliente_repo_impl import ClienteRepositorioSQLServer

print('🔍 Probando repositorio de clientes...')

try:
    db_config = DatabaseConfig()
    session = db_config.get_session()
    repo = ClienteRepositorioSQLServer(session)
    
    # Listar clientes (debería estar vacío)
    clientes = repo.listar_todos()
    print(f'✅ Clientes encontrados: {len(clientes)}')
    
    session.close()
    print('✅ Prueba de repositorio exitosa')
    
except Exception as e:
    print(f'❌ Error: {e}')
