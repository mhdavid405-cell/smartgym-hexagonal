import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.database import DatabaseConfig
from src.infrastructure.database.models.cliente_model import ClienteModel, MembresiaModel

print('🔍 Probando conexión y consulta de membresías...')

try:
    db_config = DatabaseConfig()
    session = db_config.get_session()
    
    # Probar consulta
    membresias = session.query(MembresiaModel).all()
    print(f'✅ Se encontraron {len(membresias)} membresías:')
    for m in membresias:
        print(f'  - {m.tipo}: ')
    
    session.close()
    print('✅ Prueba exitosa')
    
except Exception as e:
    print(f'❌ Error: {e}')
