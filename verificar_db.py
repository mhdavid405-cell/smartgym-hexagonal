import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv('DB_HOST', 'localhost')
username = os.getenv('DB_USER', 'sa')
password = os.getenv('DB_PASSWORD', '')
database = os.getenv('DB_NAME', 'smartgym_db')

print(f'🔌 Conectando a la base de datos {database}...')

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(conn_str)
    print(f'✅ Conexión exitosa a {database}')
    conn.close()
except Exception as e:
    print(f'❌ Error: {e}')
