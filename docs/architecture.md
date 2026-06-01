# Architecture Diagram - Simple LMS Advanced Features

## Gambaran Umum Arsitektur

Simple LMS menggunakan arsitektur microservices berbasis Docker yang terdiri dari 8 container:

- Django Ninja API (REST API)
- PostgreSQL (database relasional)
- Redis (cache & message broker)
- MongoDB (document store untuk log)
- RabbitMQ (message queue)
- Celery Worker (async task executor)
- Celery Beat (scheduled task)
- Flower (task monitoring)

## Diagram Arsitektur

```mermaid
graph TB
    subgraph "External Client"
        Client[Web Browser / Mobile App]
    end

    subgraph "Docker Host - 8 Services"

        subgraph "Web Layer"
            API[Django Ninja API :8000]
        end

        subgraph "Application Layer"
            CeleryWorker[Celery Worker]
            CeleryBeat[Celery Beat Scheduler]
            Flower[Flower Monitor :5555]
        end

        subgraph "Message Broker"
            RabbitMQ[RabbitMQ :5672]
        end

        subgraph "Data Layer"
            PostgreSQL[(PostgreSQL :5432)]
            MongoDB[(MongoDB :27017)]
            Redis[(Redis :6379)]
        end

        subgraph "File Storage"
            Media[Media Files<br/>Certificates & Reports]
        end

    end

    %% Koneksi Antar Komponen
    Client --> API

    API --> PostgreSQL
    API --> Redis
    API --> MongoDB
    API --> RabbitMQ

    RabbitMQ --> CeleryWorker
    CeleryBeat --> RabbitMQ

    CeleryWorker --> PostgreSQL
    CeleryWorker --> Redis
    CeleryWorker --> MongoDB
    CeleryWorker --> Media

    Flower --> CeleryWorker
    Flower --> RabbitMQ
```
