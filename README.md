# SmartGym - Sistema de Gestión de Gimnasio

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-2022-red.svg)](https://www.microsoft.com/sql-server)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)

Sistema completo de gestión para gimnasios con **arquitectura hexagonal**, roles de usuario (Admin/Entrenador/Cliente), CRUD completo de clientes, membresías, pagos, rutinas, dietas y seguimiento de progreso.

## Características

- ✅ **Arquitectura Hexagonal** (Puertos y Adaptadores)
- ✅ **Autenticación y Roles**: Admin, Entrenador, Cliente
- ✅ **CRUD Completo**: Clientes, Membresías, Pagos, Rutinas, Dietas, Progreso
- ✅ **API REST**: 40+ endpoints documentados
- ✅ **Frontend**: Bootstrap 5, responsive
- ✅ **Docker**: Contenedor para fácil despliegue

## Tecnologías

| Capa | Tecnología |
|------|------------|
| Backend | Python 3.12 + Flask |
| Base de datos | SQL Server 2022 |
| ORM | SQLAlchemy |
| Frontend | Bootstrap 5, Jinja2, JavaScript |
| Infraestructura | Docker |

##  Roles y Permisos

| Rol | Acceso |
|-----|--------|
| **Admin** | Acceso total a todo el sistema |
| **Entrenador** | Gestiona clientes, rutinas, dietas, progreso |
| **Cliente** | Solo visualiza su información personal |

## Instalación

### Opción 1: Local

\\\ash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/smartgym-hexagonal.git
cd smartgym-hexagonal

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Crear base de datos en SQL Server
# Ejecutar el script SQL en DBeaver o SSMS

# Ejecutar
python main.py
\\\

### Opción 2: Docker

\\\ash
# Levantar contenedor
docker-compose up -d

# Acceder a la aplicación
http://localhost:5000
\\\

## 🔗 Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | \/api/clientes\ | Listar clientes |
| POST | \/api/clientes\ | Crear cliente |
| GET | \/api/membresias\ | Listar membresías |
| POST | \/api/pagos\ | Registrar pago |
| GET | \/api/rutinas\ | Listar rutinas |
| GET | \/api/dietas\ | Listar dietas |
| GET | \/api/progreso\ | Listar progreso |
| POST | \/api/auth/login\ | Iniciar sesión |

## Estructura del Proyecto

\\\
smartgym-hexagonal/
├── src/
│   ├── domain/           # Núcleo (Entidades, Casos de Uso, Puertos)
│   ├── infrastructure/   # Adaptadores (Base de datos, Web)
│   └── config/           # Configuración
├── tests/                # Pruebas
├── main.py               # Punto de entrada
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
\\\

##  Capturas de Pantalla

| Dashboard Admin | Dashboard Entrenador | Dashboard Cliente |
|-----------------|---------------------|-------------------|
| ![Admin](docs/admin.png) | ![Entrenador](docs/entrenador.png) | ![Cliente](docs/cliente.png) |

## Licencia

MIT

## Autor

[Manzano Hernandez David Axel] - [mhdavid405@gmail.com] 

---

¡No olvides dejar una estrella si te gustó el proyecto!
