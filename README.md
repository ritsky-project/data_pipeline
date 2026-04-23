# Automated ELT Pipeline — API to Insights

## Overview

An end-to-end ELT pipeline that ingests live data from a REST API, loads raw records into PostgreSQL, applies modular transformations using dbt, orchestrates the full workflow with Apache Airflow 3.0, and surfaces business-ready dashboards via Apache Superset. The entire stack runs in Docker with full cross-platform support.

---

## Architecture

![Architecture Diagram](https://github.com/ritsky-project/data_pipeline/blob/main/images/image.png)

```
REST API
   │
   ▼
[ Python Ingestion Layer ]
   │  (raw JSON → staging)
   ▼
[ PostgreSQL — Raw Schema ]
   │
   ▼
[ dbt — Transform Layer ]
   │  (staging → intermediate → marts)
   ▼
[ PostgreSQL — Analytics Schema ]
   │
   ▼
[ Apache Superset — Dashboards ]

         ↑ All stages orchestrated by Apache Airflow 3.0
```

---

## Tech Stack

| Layer          | Technology                     |
|----------------|-------------------------------|
| Ingestion      | Python, `requests`, `psycopg2` |
| Storage        | PostgreSQL 15                  |
| Transformation | dbt Core                       |
| Orchestration  | Apache Airflow 3.0             |
| Visualization  | Apache Superset                |
| Containerization | Docker, Docker Compose       |
| Environment    | Windows / Linux                |

---

## Data Pipeline Flow

```
1. Airflow DAG triggers on schedule (cron / near-realtime polling)
2. Python operator hits REST API → parses JSON response
3. Raw records upserted into PostgreSQL raw schema
4. dbt run executes staged transformations (staging → marts)
5. dbt test validates data quality and schema contracts
6. Superset dashboards query the analytics schema live
```

---

## Folder Structure

```
project-root/
├── dags/
│   └── elt_pipeline_dag.py        # Airflow DAG definition
├── ingestion/
│   └── api_client.py              # API fetch + raw load logic
├── dbt/
│   ├── models/
│   │   ├── staging/               # Source cleaning layer
│   │   ├── intermediate/          # Business logic
│   │   └── marts/                 # Analytics-ready tables
│   ├── tests/                     # dbt data quality tests
│   └── dbt_project.yml
├── docker/
│   └── docker-compose.yml         # Full stack definition
├── superset/
│   └── dashboards/                # Exported dashboard configs
└── README.md
```

---

## Key Components

**Airflow 3.0**
- Schedules and monitors all pipeline tasks
- Uses `PythonOperator` and `BashOperator` for ingestion and dbt execution
- TaskFlow API for clean dependency management

**API Ingestion Layer**
- Stateless Python script with configurable endpoints
- Handles pagination, rate limits, and error retries
- Writes raw payloads to a dedicated `raw` schema in PostgreSQL

**dbt Transform Layer**
- Three-layer model architecture: staging → intermediate → marts
- Schema tests (`not_null`, `unique`, `accepted_values`) on all critical fields
- Incremental models for large-volume tables

**PostgreSQL**
- Dual-schema design: `raw` (append-only) and `analytics` (transformed)
- Serves as both the raw landing zone and the analytical query layer

**Apache Superset**
- Connects directly to the `analytics` schema
- Pre-built dashboards with filters, time-series charts, and KPI tiles

---

## Features

- **Near-Realtime Ingestion** — Airflow polls the API at configurable short intervals
- **Idempotent Loads** — Upsert logic prevents duplicate records on re-runs
- **Data Quality Enforcement** — dbt tests block bad data from reaching marts
- **Full Observability** — Airflow UI exposes task-level logs and run history
- **Containerized Stack** — Single `docker-compose up` runs the full environment
- **Modular Design** — Each layer is independently testable and replaceable

---

## How It Works

1. **Trigger** — Airflow DAG fires on schedule; parameters passed via Airflow Variables
2. **Extract** — `api_client.py` fetches paginated API responses; normalizes JSON to tabular format
3. **Load** — Records are bulk-inserted into PostgreSQL `raw` schema with ingestion timestamp
4. **Transform** — dbt models execute sequentially; incremental strategy updates only new rows
5. **Test** — dbt tests run post-transformation; failures halt the DAG and alert via logs
6. **Serve** — Superset reads from `analytics` marts; dashboards refresh on query

---

## Use Cases

- Operational reporting on live API data sources
- Near-realtime KPI monitoring with historical trend analysis
- Rapid prototyping of production-grade ELT pipelines
- Template base for financial, IoT, or e-commerce data platforms

---

## Skills Demonstrated

- ELT pipeline design and implementation
- dbt modular modeling and testing patterns
- Airflow DAG authoring with the TaskFlow API
- PostgreSQL schema design for analytical workloads
- Docker multi-service orchestration
- Data quality framework implementation
- REST API ingestion with fault tolerance

---

## Future Improvements

- Replace polling with webhook-based event ingestion
- Add Great Expectations for extended data quality coverage
- Migrate orchestration to Airflow with Celery executor for horizontal scaling
- Introduce a message queue (Kafka / Redis) for true streaming ingestion
- Implement CI/CD for dbt model testing on pull requests
- Add dbt documentation site auto-deployment
