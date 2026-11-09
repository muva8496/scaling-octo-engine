# ⚡ Enterprise-Grade Asynchronous Retail Backend API
> A high-throughput, non-blocking inventory and transaction processing backend engineered with **FastAPI**, **SQLAlchemy 2.0 (Async)**, **PostgreSQL**, **Alembic**, and **Pydantic v2**.

---

## 📑 Table of Contents
1. [Executive Summary & Architecture Vision](#-executive-summary--architecture-vision)
2. [Core Technology Stack](#-core-technology-stack)
3. [System Architecture & Data Flow](#-system-architecture--data-flow)
4. [Project Directory Structure](#-project-directory-structure)
5. [Prerequisites & Local Environment Setup](#-prerequisites--local-environment-setup)
6. [Database Configuration & Migration Pipelines](#-database-configuration--migration-pipelines)
7. [Running the Application](#-running-the-application)
8. [Comprehensive API Endpoints Reference](#-comprehensive-api-endpoints-reference)
9. [Error Handling & Validation Architecture](#-error-handling--validation-architecture)
10. [Production Readiness & Best Practices](#-production-readiness--best-practices)

---

## 🏛️ Executive Summary & Architecture Vision

Modern retail and high-volume e-commerce platforms demand backends capable of absorbing massive concurrent traffic spikes without thread starvation or database latency bottlenecks. This project implements a modern **Asynchronous Python Architecture** designed to decouple HTTP transport management from database input/output (I/O) wait times.

By combining **FastAPI** with an asynchronous **SQLAlchemy 2.0** session layer driven by **`asyncpg`**, the application's event loop can efficiently context-switch across thousands of concurrent client requests, ensuring maximum CPU utilization and minimal latency.

---

## 🛠️ Core Technology Stack

| Layer / Concern | Technology | Purpose / Rationale |
| :--- | :--- | :--- |
| **Web Framework** | FastAPI (Python 3.11+) | High-performance routing, automatic OpenAPI/Swagger documentation, and native async support. |
| **Data Validation** | Pydantic v2 | Strict perimeter data parsing, type enforcement, and automated JSON serialization. |
| **ORM / Database Toolkit** | SQLAlchemy 2.0 (Async) | Modern type-safe database mapping using `Mapped` and `mapped_column` declarations with non-blocking execution engines. |
| **Database Driver** | `asyncpg` | C-optimized, ultra-fast asynchronous PostgreSQL driver for Python. |
| **Database Engine** | PostgreSQL 18+ | Robust, ACID-compliant relational data store capable of handling complex retail ledgers. |
| **Migration Management** | Alembic | Version-controlled database schema migrations decoupled from application runtime. |
| **ASGI Server** | Uvicorn | Blazing-fast production ASGI server implementation with hot-reload capabilities. |

---

## 🔄 System Architecture & Data Flow

```text
 [ Client / Frontend / Swagger UI ]
                 │
                 ▼ (HTTP POST / GET / PUT / DELETE with JSON Payload)
     [ FastAPI Route Handler ]
                 │
                 ▼ (Perimeter Validation via Pydantic Schemas)
    [ Request-Scoped Async Session Dependency (`get_db`) ]
                 │
                 ▼ (Non-Blocking Transaction Execution via asyncpg)
        [ PostgreSQL Database Cluster ]