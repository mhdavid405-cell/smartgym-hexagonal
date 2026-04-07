# SmartGym — PRODUCT.md

> Este documento existe para explicar el **por qué** detrás de cada decisión técnica y de producto.
> Es tan importante como el código. Un sistema sin contexto es solo archivos.

---

## El problema que resuelve

Un gimnasio pequeño o mediano (1-5 entrenadores, hasta 200 clientes) necesita gestionar
membresías, pagos, rutinas de entrenamiento, dietas y seguimiento de progreso físico.
Sin un sistema, esto se hace en hojas de cálculo o papel: el entrenador no sabe qué rutina
tiene cada cliente, el admin no sabe quién debe su mensualidad, y el cliente no ve su evolución.

**Problema central:** no existe un lugar único donde el admin vea el negocio, el entrenador
gestione el trabajo con sus clientes, y el cliente consulte su información — todo con
el nivel de acceso apropiado para cada rol.

**Usuarios:**
- **Admin**: ve el negocio completo — clientes, ingresos, membresías, usuarios del sistema
- **Entrenador**: gestiona a sus clientes — rutinas, dietas, progreso físico
- **Cliente**: consulta su información — membresía, rutina activa, dieta, historial

---

## Decisiones de producto

### ¿Por qué 3 roles y no uno solo?

Un sistema de gimnasio tiene flujos de trabajo radicalmente distintos por usuario.
El admin necesita ver reportes y gestionar membresías. El entrenador necesita
ver la lista de sus clientes y asignarles rutinas. El cliente no necesita ver
información de otros clientes ni crear rutinas.

Un solo rol implicaría que el cliente podría ver datos sensibles de otros,
o que el entrenador podría borrar usuarios accidentalmente. Los roles no son
una feature — son una restricción de seguridad necesaria.

### ¿Por qué bcrypt para passwords y no MD5?

El consultorio médico anterior usaba MD5. SmartGym usa bcrypt.
Esa diferencia no es cosmética: MD5 es trivialmente rompible con tablas arcoíris.
bcrypt incorpora un salt automático y un factor de costo que escala con el hardware.
Cualquier sistema que guarda passwords de usuarios reales debe usar bcrypt o similar.

### ¿Por qué validar el monto del pago contra el precio de la membresía en el dominio?

La regla "el monto pagado debe ser igual al precio de la membresía" es una regla de negocio,
no de la interfaz. Si esta validación estuviera solo en el frontend, cualquier llamada
directa a la API podría saltarla. Al estar en `gestionar_pago.py` (capa de dominio),
es imposible registrar un pago incorrecto sin importar cómo se llame al sistema.

### ¿Por qué registrar la medición más reciente y calcular evolución?

El seguimiento de progreso tiene dos usuarios con necesidades distintas:
el entrenador necesita ver si el cliente está progresando hacia su objetivo,
el cliente necesita motivación visible.

La decisión de calcular evolución como `último - primero` (no como porcentaje)
es deliberada: mostrar "bajaste 3.5 kg" es más motivador y procesable que
"bajaste 4.2% de tu peso inicial".

### Features descartadas del MVP

| Feature | Razón del descarte |
|---|---|
| Notificaciones de vencimiento de membresía | Requiere scheduler (Celery/APScheduler) y canal de envío (email/WhatsApp). Alta complejidad para V1 |
| Aplicación móvil | Web responsive cumple el caso de uso. App nativa sería V3 si hay demanda |
| Integración con wearables / Garmin / Apple Watch | API de terceros + sincronización en tiempo real. Candidato para V2 si hay demanda |
| Dashboard con gráficas de evolución | El valor está en el registro primero. Gráficas en V1.1 cuando haya suficientes datos |
| Sistema de clases grupales / calendario | Módulo separado con lógica de cupos y horarios. V2 |
| Facturación / notas fiscales | Requiere integración con SAT (México) o sistema fiscal local. Fuera del alcance |
| Modo dark | No agrega valor funcional en V1 |

### ¿Por qué mantener `scripts/` en el repo?

Los scripts de `crear_db.py`, `crear_tablas.py`, `verificar_db.py` son herramientas
de setup y debugging que cualquier desarrollador nuevo necesita al configurar el entorno.
Pertenecen al repo como documentación ejecutable, pero claramente separados en `scripts/`
para que no se confundan con código de producción.

Lo que no debe estar en el repo: el `venv/`, los `__pycache__/`, y los tests de integración
que hacen `requests.post` a `localhost:5000` (eso requiere el servidor corriendo y es frágil).

---

## Decisiones de arquitectura

### ¿Por qué Arquitectura Hexagonal en un proyecto de esta escala?

SmartGym tiene 7 entidades de dominio, 40+ endpoints, y 3 capas de usuario con
lógica de negocio diferente por cada una. A esta escala, la arquitectura hexagonal
empieza a pagar dividendos: los tests de dominio corren en milisegundos sin base de datos,
agregar un nuevo endpoint no requiere tocar el dominio, y cambiar SQL Server por PostgreSQL
sería cambiar solo `src/config/database.py`.

Sin esta separación, el sistema degeneraría en código espagueti a la segunda semana.

### ¿Por qué SQLAlchemy en lugar de pyodbc raw?

El consultorio médico usó pyodbc raw. SmartGym usa SQLAlchemy.
pyodbc obliga a escribir SQL manualmente para cada operación, duplicando código y
aumentando el riesgo de errores. SQLAlchemy con el patrón repositorio da:
- Type safety via los modelos
- Transacciones manejadas por el ORM
- Independencia de base de datos (cambiar SQL Server por PostgreSQL = cambiar la connection string)

La decisión de usar `session.merge()` en lugar de `session.add()` en los repositorios
es deliberada: `merge` actualiza si existe, inserta si no — un upsert natural para el patrón repositorio.

### ¿Por qué decoradores para la autenticación?

`@login_requerido`, `@admin_requerido`, `@entrenador_requerido` son decoradores
en `decorators.py`. Esto permite aplicar restricciones de acceso en una línea sin
repetir lógica de verificación de sesión en cada función. Si mañana la lógica de
autenticación cambia, se cambia en un solo lugar.

### La decisión de usar `session` de Flask en lugar de JWT

Para una aplicación web con frontend renderizado en servidor (Jinja2), las sesiones
de Flask son más simples y suficientes. JWT tendría sentido si el frontend fuera
una SPA en React o si hubiera una app móvil consumiendo la API.
La arquitectura hexagonal facilita migrar a JWT en V2 sin tocar el dominio.

### El problema de las relaciones circulares en SQLAlchemy

Durante el desarrollo, las relaciones entre `ClienteModel`, `PagoModel`, `RutinaModel`
y `DietaModel` generaban errores de carga circular. La solución fue eliminar las
`relationship()` en los modelos que causaban el ciclo y resolver las consultas
cruzadas directamente desde el repositorio con SQL explícito.

Esto es documentado porque es una trampa común en proyectos con SQLAlchemy:
las relaciones bidireccionales entre 4+ modelos pueden generar ciclos de importación
que son difíciles de debuggear. Mantener las relaciones mínimas y resolver
las joins desde el repositorio es más predecible.

---

## Cómo medir el éxito del MVP

| Métrica | Objetivo | Cómo medirla |
|---|---|---|
| Tiempo de registro de nuevo cliente | < 3 minutos | Cronometrar con admin real |
| Tiempo de asignación de rutina | < 2 minutos | Cronometrar con entrenador |
| Errores al registrar medidas de progreso | 0 por sesión | Observar al entrenador usando el sistema |
| Clientes que consultan su dashboard | > 60% de los registrados | Log de sesiones por rol |

---

## Roadmap

- **V1 (entregado):** gestión de clientes, membresías, pagos, rutinas, dietas, progreso, roles, Docker
- **V1.1:** gráficas de evolución de progreso, export CSV de clientes, búsqueda en tablas
- **V2:** dashboard con métricas del negocio, notificaciones de membresías por vencer, módulo de clases grupales
- **V3 (si hay demanda):** app móvil, integración con pasarela de pagos, facturación

---

## Reflexión

SmartGym fue construido inmediatamente después del consultorio médico. La diferencia
en calidad es visible: bcrypt en lugar de MD5, SQLAlchemy en lugar de SQL raw,
decoradores en lugar de verificaciones repetidas, GitHub Actions para CI/CD.

Cada proyecto de portafolio debe mostrar que aprendiste algo del anterior.
Esa progresión es la narrativa más honesta que puedes mostrar en una entrevista.
