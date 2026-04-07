# 🏋️ SmartGym — Sistema de Gestión de Gimnasio

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-2022-red.svg)](https://www.microsoft.com/sql-server)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Hexagonal-purple.svg)]()
[![Tests](https://img.shields.io/badge/Tests-pytest-yellow.svg)](https://pytest.org)

> Sistema completo de gestión para gimnasios con **Arquitectura Hexagonal (Puertos y Adaptadores)**,
> sistema de roles (Admin / Entrenador / Cliente), API REST con 40+ endpoints,
> autenticación con bcrypt y frontend Bootstrap 5 responsive.

> Ver [PRODUCT.md](./PRODUCT.md) para entender las decisiones de producto y arquitectura.

---

## 📸 Capturas de Pantalla

| Home | Login | Dashboard Admin |
|---|---|---|
| ![Home](docs/images/home.png) | ![Login](docs/images/login.png) | ![Admin](docs/images/admin.png) |

| Dashboard Entrenador | Dashboard Cliente |
|---|---|
| ![Entrenador](docs/images/entrenador.png) | ![Cliente](docs/images/cliente.png) |

---

## ✅ Funcionalidades

- **Autenticación con roles**: Admin, Entrenador y Cliente — sesiones seguras con bcrypt
- **CRUD de Clientes**: registro, edición, baja lógica, asignación de membresías
- **Membresías**: 3 planes (Básica, VIP, Premium) con precios y duración
- **Pagos**: registro de pagos, validación contra precio de membresía, actualización automática del cliente
- **Rutinas**: asignación de rutinas de entrenamiento por cliente, activar/desactivar
- **Dietas**: planes alimenticios por cliente con historial
- **Progreso**: registro de medidas corporales periódicas y cálculo de evolución
- **API REST**: 40+ endpoints organizados por módulos con autenticación por sesión
- **CI/CD**: GitHub Actions corre tests de dominio en cada push
- **Docker**: levanta todo con un comando

---

## 🧠 Arquitectura Hexagonal

El sistema está organizado bajo el patrón de **Puertos y Adaptadores**, separando claramente:

- **Domain** (`src/domain/`): lógica de negocio pura — entidades, interfaces, casos de uso
- **Infrastructure** (`src/infrastructure/`): adaptadores de BD (SQLAlchemy) y web (Flask)
- **Config** (`src/config/`): configuración de conexión, lee siempre desde variables de entorno

**Regla central:** el dominio nunca sabe que Flask o SQL Server existen.
Si mañana migras a FastAPI o PostgreSQL, solo cambia el adaptador — el dominio no se toca.

```
src/
├── domain/
│   ├── entities/              # Cliente, Rutina, Dieta, Progreso, Pago, Usuario
│   ├── interfaces/
│   │   └── repositorios/      # Contratos abstractos que el dominio necesita
│   └── use_cases/             # GestionarCliente, GestionarRutina, AutenticarUsuario...
├── infrastructure/
│   ├── database/
│   │   ├── models/            # Modelos SQLAlchemy (ORM)
│   │   └── repositories/      # Implementaciones concretas de los repositorios
│   └── web/
│       ├── controllers/       # Blueprints Flask — solo serialización y routing
│       ├── decorators.py      # login_requerido, admin_requerido, entrenador_requerido
│       ├── static/            # CSS y JS
│       └── templates/         # Jinja2 con dashboards por rol
└── config/
    └── database.py            # DatabaseConfig — lee credenciales desde .env
```

---

## 🏗️ Tecnologías

| Capa | Tecnología | Razón |
|---|---|---|
| Backend | Python 3.12 + Flask 2.3 | Ligero, sin magia, cada decisión visible |
| Base de datos | SQL Server 2022 | Entorno disponible, SQLAlchemy facilita migración |
| ORM | SQLAlchemy 2.0 | Mapeo objeto-relacional sin SQL raw innecesario |
| Autenticación | bcrypt | Hashing seguro de passwords, estándar de la industria |
| Frontend | Bootstrap 5 + Jinja2 | UI funcional responsive sin sobreingeniería |
| Tests | pytest | Suite de dominio sin base de datos — rápida y confiable |
| CI/CD | GitHub Actions | Tests automáticos en cada push |
| Infraestructura | Docker | Despliegue reproducible en cualquier máquina |

---

## 👥 Roles y Permisos

| Rol | Acceso |
|---|---|
| 👑 **Admin** | Acceso total: clientes, usuarios, membresías, reportes, todo |
| 🏋️ **Entrenador** | Gestiona clientes, rutinas, dietas y progreso |
| 👤 **Cliente** | Solo visualiza su información personal |

---

## 🔗 API REST — Endpoints principales

| Módulo | Método | Endpoint | Descripción |
|---|---|---|---|
| Auth | POST | `/api/auth/login` | Iniciar sesión |
| Auth | POST | `/api/auth/registro` | Registrar usuario |
| Auth | POST | `/api/auth/logout` | Cerrar sesión |
| Clientes | GET | `/api/clientes` | Listar clientes |
| Clientes | POST | `/api/clientes` | Crear cliente |
| Clientes | PUT | `/api/clientes/<id>` | Actualizar cliente |
| Membresías | GET | `/api/membresias` | Listar planes |
| Pagos | POST | `/api/pagos` | Registrar pago |
| Rutinas | GET/POST | `/api/rutinas` | Listar / crear rutinas |
| Rutinas | GET | `/api/rutinas/cliente/<id>/activa` | Rutina activa del cliente |
| Dietas | GET/POST | `/api/dietas` | Listar / crear dietas |
| Progreso | POST | `/api/progreso` | Registrar medidas |
| Progreso | GET | `/api/progreso/cliente/<id>/evolucion` | Calcular evolución |

---

## 🚀 Instalación

### Prerequisitos
- Docker Desktop instalado y corriendo
- SQL Server local con la base de datos `smartgym_db` creada

### 1. Clonar el repositorio
```bash
git clone https://github.com/mhdavid405-cell/smartgym-hexagonal.git
cd smartgym-hexagonal
```

### 2. Configurar variables de entorno
```bash
cp .env.example .env
# Edita .env con tus credenciales de SQL Server
```

### 3. Crear tablas en la base de datos
```bash
python scripts/crear_tablas.py
```

### 4. Levantar con Docker
```bash
docker-compose up -d
# Abrir en: http://localhost:5000
```

### Sin Docker (desarrollo local)
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac
pip install -r requirements.txt
python main.py
```

---

## 🧪 Tests

Los tests de dominio corren **sin base de datos** usando clases concretas en memoria:

```bash
pip install -r requirements.txt
pytest tests/test_cliente_domain.py -v
```

Los tests de dominio validan: creación de entidades, reglas de negocio, cálculo de vencimiento de membresía.

---

## 👤 Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador |
| `entrenador1` | `admin123` | Entrenador |
| `cliente1` | `admin123` | Cliente |

> ⚠️ Solo para entorno local de pruebas.

---

## 📄 Licencia

MIT

---

## 👨‍💻 Autor

**Manzano Hernandez David Axel**
📧 mhdavid405@gmail.com
🐙 [github.com/mhdavid405-cell](https://github.com/mhdavid405-cell)

Sistema construido como proyecto de portafolio para demostrar conocimiento de
Arquitectura Hexagonal, Python, Flask, SQL Server, Docker y buenas prácticas
de desarrollo orientado a producto.

⭐️ Si te fue útil, deja una estrella al repo.
