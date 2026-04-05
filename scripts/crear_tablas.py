import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv('DB_HOST', 'localhost')
username = os.getenv('DB_USER', 'sa')
password = os.getenv('DB_PASSWORD', '')
database = os.getenv('DB_NAME', 'smartgym_db')

print(f'🔌 Conectando a {database}...')

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Crear tabla de membresías
print('📦 Creando tabla membresias...')
cursor.execute('''
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='membresias' AND xtype='U')
CREATE TABLE membresias (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL UNIQUE,
    precio DECIMAL(10,2) NOT NULL,
    descripcion TEXT,
    duracion_dias INT DEFAULT 30
)
''')

# Crear tabla de clientes
print('📦 Creando tabla clientes...')
cursor.execute('''
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='clientes' AND xtype='U')
CREATE TABLE clientes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    fecha_registro DATE NOT NULL,
    activo BIT DEFAULT 1,
    membresia_id INT,
    fecha_vencimiento_membresia DATE,
    FOREIGN KEY (membresia_id) REFERENCES membresias(id)
)
''')

# Insertar membresías
print('📦 Insertando tipos de membresía...')
cursor.execute('''
IF NOT EXISTS (SELECT * FROM membresias)
BEGIN
    INSERT INTO membresias (tipo, precio, descripcion) VALUES
    ('BÁSICA', 600.00, 'Acceso a sala de pesas y cardio'),
    ('VIP', 700.00, 'Acceso total + área de spa y clases grupales'),
    ('PREMIUM', 1200.00, 'Acceso total + spa + 1 sesión de entrenador personal')
END
''')

conn.commit()
print('✅ Tablas creadas y datos insertados correctamente')
conn.close()
