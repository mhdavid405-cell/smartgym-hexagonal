import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv('DB_HOST', 'localhost')
username = os.getenv('DB_USER', 'sa')
password = os.getenv('DB_PASSWORD', '')
database = os.getenv('DB_NAME', 'smartgym_db')

print(f'🔌 Conectando al servidor {server}...')

# Conectar al servidor
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
conn.autocommit = True
cursor = conn.cursor()

# Crear base de datos si no existe
print(f'📦 Creando base de datos {database} si no existe...')
cursor.execute(f'''
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{database}')
BEGIN
    CREATE DATABASE [{database}]
END
''')

print(f'✅ Base de datos {database} creada/verificada')
conn.close()
