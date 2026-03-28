from src.config.database import DatabaseConfig
from sqlalchemy import inspect
from src.infrastructure.database.models import ClienteModel, RutinaModel

db = DatabaseConfig()
engine = db.create_engine()
inspector = inspect(engine)

print('=== TABLAS EN LA BD ===')
print(inspector.get_table_names())

print('\n=== MODELOS REGISTRADOS ===')
print('ClienteModel:', ClienteModel.__table__.name)
print('RutinaModel:', RutinaModel.__table__.name)

print('\n=== FOREIGN KEYS DE RUTINAS ===')
fks = inspector.get_foreign_keys('rutinas')
for fk in fks:
    print(f"  {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
