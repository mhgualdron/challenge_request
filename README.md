# Invoice Management System — Challenge Técnico Backend - AI

Esta solución representa una implementación robusta y escalable para la gestión de facturas, diseñada bajo los más altos estándares de ingeniería de software. El proyecto integra una arquitectura limpia (**Clean Architecture**), principios **SOLID** y una estrategia de persistencia de datos de alto rendimiento basada en **Stored Procedures**.

---

## 🏛️ Arquitectura y Decisiones de Diseño

La aplicación se rige por un enfoque **Feature-Based** con un núcleo (**Core**) transversal, garantizando una separación de responsabilidades absoluta:

### Principios Fundamentales
*   **Clean Architecture:** El dominio y la lógica de negocio son independientes de los frameworks y la base de datos.
*   **Procedural Data Access:** Siguiendo los requerimientos, la persistencia se delega enteramente a **Stored Procedures** en MS SQL Server. SQLAlchemy se utiliza exclusivamente como administrador de conexiones (**Connection Pool**), eliminando la sobrecarga de un ORM para las consultas.
*   **Inversion of Control (IoC):** Implementación de **Dependency Injection** nativa de FastAPI para desacoplar los routers de las implementaciones concretas de los repositorios.
*   **Domain-Driven Exceptions:** Gestión de errores centralizada mediante excepciones de dominio mapeadas a respuestas HTTP semánticas.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
| :--- | :--- |
| **Lenguaje** | Python 3.11+ |
| **Framework Web** | FastAPI |
| **Validación** | Pydantic v2 |
| **Base de Datos** | Microsoft SQL Server 2022 |
| **Driver DB** | PyODBC / PyMSSQL |
| **Persistencia** | SQLAlchemy Core (Execute Text) |
| **Seguridad** | OAuth2 + JWT (Bearer Token) |
| **Contenedores** | Docker & Docker Compose |

---

## 🚀 Despliegue y Configuración

### 1. Inicialización del Entorno
El proyecto está completamente containerizado para asegurar la paridad entre entornos.

```bash
# Construir e iniciar servicios (Database & API)
docker-compose up -d --build
```
*Nota: El servicio de la API incluye un mecanismo de espera (Healthcheck) que garantiza que el SQL Server esté listo para aceptar conexiones antes de iniciar.*

### 2. Ciclo de Vida de Base de Datos
Las migraciones están gestionadas por **Alembic**, divididas en esquemas, índices y lógica procedural.

```bash
# Ejecutar migraciones y poblar datos semilla
docker exec -it invoice_api poetry run alembic upgrade head
```

---

## 📖 Interfaz de Programación (API)

### Autenticación
Todos los endpoints de facturas requieren un token JWT válido.
- **Login:** `POST /auth/token` (Credentials: `admin` / `password123`)

### Catálogo de Endpoints
- **Operaciones de Factura:**
    - `POST /invoice/` - Registro integral de factura.
    - `GET /invoice/{id}` - Recuperación de registro por PK.
    - `GET /invoice/search?client={name}` - Búsqueda optimizada por cliente (LIKE).

*Documentación interactiva disponible en:* [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📊 Documentación Avanzada

Este challenge se complementa con dos análisis técnicos profundos:

1.  **[Prompt Engineering & LLM Optimization](docs/PROMPTS.md):** Un estudio detallado sobre la transformación de clausulados de seguros densos en resúmenes estructurados utilizando técnicas de **Few-Shot**, **CoT** y **Negative Constraints**, validado con resultados reales de GPT.
2.  **[Estrategia de Pruebas Volumétricas](docs/VOLUMETRIC_TESTING.md):** Diseño de una infraestructura de carga masiva en **AWS** (ECS, SQS, RDS) capaz de procesar **100 millones de registros**, incluyendo scripts de **Locust** y diagramas de arquitectura en **PlantUML**.

---

## 🧪 Calidad y Verificación

El proyecto mantiene una suite de pruebas automatizadas que validan tanto la integridad de los esquemas como la lógica de negocio:

```bash
# Ejecución de tests unitarios e integración
export PYTHONPATH="."
poetry run pytest
```