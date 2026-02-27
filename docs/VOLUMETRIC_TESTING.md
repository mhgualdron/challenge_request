# Estrategia de Pruebas Volumétricas: Microservicio de Facturas

Este documento define el plan estratégico para validar la escalabilidad, estabilidad y resiliencia de la API de facturas ante grandes volúmenes de datos y concurrencia masiva.

## 1. Definiciones de Pruebas

A continuación se presenta la tabla comparativa para diferenciar el alcance de cada tipo de prueba:

| Tipo de Prueba | Objetivo Principal | Volumen / Carga | Resultado Esperado |
| :--- | :--- | :--- | :--- |
| **Carga (Load)** | Validar el comportamiento bajo la carga esperada de producción. | 1.000 concurrentes (Nominal). | Respuesta dentro de SLAs (p95 < 200ms). |
| **Estrés (Stress)** | Encontrar el punto de ruptura del sistema. | 10.000+ concurrentes (Hasta el fallo). | Identificación del componente que colapsa primero. |
| **Volumétrica** | Medir el rendimiento cuando la DB crece masivamente. | 100M+ de registros en tabla `invoices`. | Estabilidad en tiempos de respuesta a pesar del tamaño de la data. |

---

## 2. Escenario de Prueba Realista

Se simulará un cierre de mes donde múltiples sistemas ERP registran facturas simultáneamente y el equipo contable realiza búsquedas masivas.

- **Volumen de Base de Datos Base:** 50.000.000 registros pre-insertados.
- **Tasa de Inserción Objetivo:** 2.000 facturas/segundo (TPS).
- **Concurrencia:** 5.000 usuarios virtuales simulados.
- **Duración Total:** 1 hora.

---

## 3. Métricas y KPIs (Umbrales de Aceptación)

| Métrica | KPI (Umbral Máximo/Mínimo) | Descripción |
| :--- | :--- | :--- |
| **Latencia p95** | < 250 ms | El 95% de las peticiones deben ser rápidas. |
| **Latencia p99** | < 800 ms | Control de "long-tail" latencies en búsquedas pesadas. |
| **Error Rate** | < 0.5% | Porcentaje de fallos HTTP (5xx) permitidos. |
| **Throughput** | > 2.500 req/sec | Capacidad total de procesamiento del cluster. |
| **CPU/RAM DB** | < 75% | Evitar saturación del motor SQL Server. |

---

## 4. Estrategia de Ejecución por Fases

| Fase | Duración | Carga (Usuarios) | Propósito |
| :--- | :--- | :--- | :--- |
| **Warmup** | 5 min | 0 -> 500 | Calentamiento de connections pool y caches. |
| **Ramp-up** | 10 min | 500 -> 5.000 | Incremento gradual para observar degradación lineal. |
| **Sustained Load** | 35 min | 5.000 | Medición de estabilidad y fugas de memoria. |
| **Spike** | 5 min | 12.000 | Simulación de ráfaga extrema inesperada. |
| **Teardown** | 5 min | 5.000 -> 0 | Liberación de recursos y consolidación de logs. |

---

## 5. Pseudo-implementación con Locust

```python
from locust import HttpUser, task, between, events
import random

class InvoiceVolumetricUser(HttpUser):
    wait_time = between(0.5, 2)
    token = None

    def on_start(self):
        """Autenticación inicial para obtener el Bearer Token."""
        auth_response = self.client.post("/auth/token", data={
            "username": "admin",
            "password": "password123"
        })
        self.token = auth_response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(10)  # Frecuencia alta para escritura
    def create_invoice(self):
        inv_num = f"VOL-{random.randint(1000000, 9999999)}"
        payload = {
            "invoice_number": inv_num,
            "client_name": "Corporativo " + str(random.randint(1, 1000)),
            "client_id": f"NIT-{random.randint(1000, 9999)}",
            "total_amount": round(random.uniform(100.0, 50000.0), 2),
            "issue_date": "2026-03-01",
            "status": "PENDING"
        }
        self.client.post("/invoice/", json=payload, headers=self.headers, name="POST /invoice")

    @task(5)
    def search_by_client(self):
        # Búsqueda parcial que fuerza el uso del Indice IX_Invoices_ClientName
        clients = ["Acme", "Globex", "Sura", "Tech"]
        query = random.choice(clients)
        self.client.get(f"/invoice/search?client={query}", headers=self.headers, name="GET /invoice/search")

    @task(2)
    def get_by_id(self):
        # Consulta por PK (Extremadamente rápida en SQL Server)
        inv_id = random.randint(1, 100000)
        self.client.get(f"/invoice/{inv_id}", headers=self.headers, name="GET /invoice/{id}")
```

---

## 6. Arquitectura de Infraestructura de Prueba (AWS)

```text
[ Locust Cluster (Distributed) ]
           |
           v (HTTPS)
[ AWS API Gateway ] <---> [ AWS WAF (Web App Firewall) ]
           |
           v
[ Application Load Balancer (ALB) ]
           |
           +-----> [ ECS Fargate Service (API Cluster Auto-scaled) ]
           |           |
           |           v (Asynchronous Load via SQS)
           |       [ SQS Queue: invoice-load-buffer ]
           |           |
           |           v (Consumers)
           |       [ RabbitMQ / Celery Workers ] ----+
           |                                         |
           +-----------------------------------------+
                               |
                               v (Stored Procedures ONLY)
                  [ RDS SQL Server (High Memory Instance) ]
                               |
                               +--> [ AWS X-Ray: Tracing ]
                               +--> [ CloudWatch: Metrics/Logs ]
```

### Integración de Componentes:
- **SQS/RabbitMQ:** Actúan como amortiguador (buffer) para absorber picos de tráfico de escritura, evitando que la base de datos se bloquee por exceso de conexiones concurrentes.
- **AWS X-Ray:** Permite visibilizar en qué Stored Procedure o capa de la red se está perdiendo tiempo durante las peticiones de alta carga.

---

## 7. Cuellos de Botella Esperados y Mitigaciones

1.  **Saturación del Pool de Conexiones:**
    - *Problema:* El motor SQL Server alcanza el `Max Connections`.
    - *Solución:* Implementar un mediador como **PgBouncer** (o equivalente de SQL Server) y aumentar el `pool_size` en SQLAlchemy.
2.  **Table Scan en Búsquedas LIKE:**
    - *Problema:* `client_name LIKE '%name%'` no usa el índice eficientemente al inicio de la cadena.
    - *Solución:* Cambiar a **Full-Text Search (FTS)** en SQL Server o implementar **ElasticSearch** como índice secundario.
3.  **Mora en la Escritura (Deadlocks):**
    - *Problema:* Alta tasa de `INSERT` concurrentes genera bloqueos en las páginas de datos.
    - *Solución:* Utilizar `SET NOCOUNT ON` en SPs y optimizar el `FILLFACTOR` de los índices.

---

## 8. Criterios de Éxito / Fallo

- **ÉXITO:** El sistema mantiene el Throughput > 2.000 TPS durante 30 minutos constantes sin que el p95 exceda los 350ms.
- **FALLO:** El Error Rate supera el 1% en cualquier fase sostenida o la base de datos entra en estado de `Deadlock` impidiendo lecturas.
