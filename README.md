# Invoice Management System - Challenge Técnico Backend

Esta solución representa una implementación robusta y escalable para la gestión de facturas, diseñada bajo los más altos estándares de ingeniería de software. El proyecto integra una arquitectura limpia (**Clean Architecture**), principios **SOLID** y una estrategia de persistencia de datos de alto rendimiento basada en **Stored Procedures**.

---

## Arquitectura y Decisiones de Diseño

La aplicación se rige por un enfoque **Feature-Based** con un núcleo (**Core**) transversal, garantizando una separación de responsabilidades absoluta:

### Principios Fundamentales
*   **Clean Architecture:** El dominio y la lógica de negocio son independientes de los frameworks y la base de datos.
*   **Procedural Data Access:** Siguiendo los requerimientos, la persistencia se delega enteramente a **Stored Procedures** en MS SQL Server. SQLAlchemy se utiliza exclusivamente como administrador de conexiones (**Connection Pool**), eliminando la sobrecarga de un ORM para las consultas.
*   **Inversion of Control (IoC):** Implementación de **Dependency Injection** nativa de FastAPI para desacoplar los routers de las implementaciones concretas de los repositorios.
*   **Domain-Driven Exceptions:** Gestión de errores centralizada mediante excepciones de dominio mapeadas a respuestas HTTP semánticas.

---

## Stack Tecnológico

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

## Despliegue y Configuración

### 1. Inicialización del Entorno
El proyecto está completamente containerizado para asegurar la paridad entre entornos.

```bash
# Construir e iniciar servicios (Database & API)
docker-compose up -d --build
```
*Nota: El servicio de la API incluye un mecanismo de espera (Healthcheck) que garantiza que el SQL Server esté listo para aceptar conexiones antes de iniciar.*

### 2. Ciclo de Vida de Base de Datos
Las migraciones están gestionadas por **Alembic**, divididas en esquemas, índices y lógica procedural.

> [!IMPORTANT]  
> SQL Server requiere que la base de datos exista antes de que Alembic pueda conectarse. Ejecute los siguientes comandos en orden:

```bash
# 1. Crear la base de datos en el contenedor
docker exec -it mssql_db /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P Challenge123! \
  -Q "CREATE DATABASE challenge_db" -C

# 2. Ejecutar migraciones y poblar datos semilla
docker exec -it invoice_api poetry run alembic upgrade head
```

---

## Acceso y Seguridad

El sistema utiliza **OAuth2 con JWT (JSON Web Tokens)** para proteger los recursos. Todos los endpoints de gestión de facturas requieren una cabecera de autorización válida.

### Credenciales de Acceso (Entorno de Desarrollo)
Para facilitar las pruebas, se ha configurado un usuario administrador por defecto:
- **Usuario:** `admin`
- **Contraseña:** `password123`

### Procedimiento de Autenticación
1. Obtener el token enviando las credenciales al endpoint de autenticación:
   ```bash
   curl -X POST "http://localhost:8000/auth/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin&password=password123"
   ```
2. Utilice el `access_token` recibido en las peticiones a la API de facturas:
   ```bash
   Authorization: Bearer <su_token_aqui>
   ```

---

## Interfaz de Programación (API)

La documentación interactiva completa (Swagger UI) está disponible en: [http://localhost:8000/docs](http://localhost:8000/docs)

### Catálogo de Endpoints Principales
- **POST /invoice/**: Registro integral de una nueva factura.
- **GET /invoice/{id}**: Recuperación de un registro específico por su identificador único.
- **GET /invoice/search?client={name}**: Búsqueda filtrada por nombre de cliente utilizando el procedimiento almacenado optimizado.

---

## Documentación Avanzada

Este challenge se complementa con dos análisis técnicos profundos:

1.  **[Prompt Engineering & LLM Optimization](docs/PROMPTS.md):** Un estudio detallado sobre la transformación de clausulados de seguros densos en resúmenes estructurados utilizando técnicas de **Few-Shot**, **CoT** y **Negative Constraints**, validado con resultados reales de GPT.
2.  **[Estrategia de Pruebas Volumétricas](docs/VOLUMETRIC_TESTING.md):** Diseño de una infraestructura de carga masiva en **AWS** (ECS, SQS, RDS) capaz de procesar **100 millones de registros**, incluyendo scripts de **Locust** y diagramas de arquitectura en **PlantUML**.

---

## Calidad y Verificación

El proyecto incluye una suite de pruebas para asegurar la integridad de la lógica de negocio y los contratos de la API:

```bash
# Ejecución de pruebas unitarias y de integración
export PYTHONPATH="."
poetry run pytest
```

---

## Propuestas de Mejora y Escalabilidad

Tras la implementación inicial, se identifican las siguientes oportunidades para robustecer la solución en un entorno de producción de alta demanda:

1. **Capa de Caché Distribuida:** Implementar **Redis** para almacenar los resultados de búsquedas frecuentes por cliente, reduciendo la carga de lectura sobre SQL Server.
2. **Procesamiento Asíncrono de Escritura:** Introducir un broker de mensajería (como **RabbitMQ** o **Amazon SQS**) para encolar la creación de facturas. Esto permitiría desacoplar la API del tiempo de respuesta de la base de datos y manejar picos de tráfico.
3. **Observabilidad Avanzada:** Integrar logs estructurados y métricas personalizadas (Prometheus/Grafana) para monitorear el rendimiento de los Stored Procedures en tiempo real.
4. **Seguridad Robusta:** Implementar **Refresh Tokens** y rotación de claves secretas, además de integrar un proveedor de identidad modular (IdP) para una gestión de usuarios más compleja.
5. **Estrategia de Particionamiento:** Para volúmenes superiores a los 100 millones de registros, se sugiere evaluar el particionamiento de tablas en SQL Server basado en rangos de fechas (Issue Date).