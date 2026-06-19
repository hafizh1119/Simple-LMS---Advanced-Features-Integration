# Testing Results

Architecture Diagram

```mermaid
graph TD

    User[User]

    User --> Django[Django API]

    Django --> PostgreSQL[(PostgreSQL)]
    Django --> Redis[(Redis Cache & Rate Limiting)]
    Django --> MongoDB[(MongoDB)]

    Django --> Celery[Celery Tasks]

    Celery --> Email[send_enrollment_email]
    Celery --> Certificate[generate_certificate]
    Celery --> Report[export_course_report]
    Celery --> Statistics[update_course_statistics]

    Flower[Flower Monitoring] --> Celery

    MongoDB --> ActivityLogs[activity_logs]
    MongoDB --> LearningAnalytics[learning_analytics]

    RabbitMQ[RabbitMQ Management]
```

## Caching Strategy - Redis

Sistem menggunakan Redis sebagai caching layer untuk mengurangi query ke PostgreSQL dan meningkatkan performa API.

### Endpoint yang Di-cache

| Endpoint                  | Key Pattern           | TTL     |
| ------------------------- | --------------------- | ------- |
| `GET /api/courses-cached` | `courses:list:{hash}` | 5 menit |
| `GET /api/courses/{id}`   | `course:{id}`         | 5 menit |

### Alur Caching

```mermaid
sequenceDiagram
    actor User
    participant API as Django API
    participant Redis as Redis Cache
    participant DB as PostgreSQL Database

    User->>API: Request Course Data
    API->>Redis: Check Cache Key

    alt Cache Hit
        Redis-->>API: Cached Data
        API-->>User: Return Response
    else Cache Miss
        Redis-->>API: Cache Not Found
        API->>DB: Query Course Data
        DB-->>API: Return Result
        API->>Redis: Save Cache (TTL 5 Minutes)
        API-->>User: Return Response
    end
```

### Cache Invalidation Strategy

Cache akan dihapus ketika data course mengalami perubahan.

```mermaid
flowchart LR
    A[Create Course] --> B[Delete Course List Cache]
    C[Update Course] --> D[Delete Course List Cache]
    C --> E[Delete Course Detail Cache]
    F[Delete Course] --> G[Delete Course List Cache]
    F --> H[Delete Course Detail Cache]
```

Implementasi cache invalidation dilakukan menggunakan:

```python
cache.delete_pattern("courses:list:*")
cache.delete(f"course:{id}")
```

## Redis Cache

Bukti Course List Cache dan Course Detail Cache.

![Redis Cache](docs/images/redis-cache.png)

Terlihat key cache:

- simple_lms:1:courses:list:...
- simple_lms:1:course:1

---

## Task Flow Documentation

### 1. Enrollment Email Task

Task ini dijalankan ketika mahasiswa berhasil melakukan enrollment course.

```mermaid
flowchart LR
    A[Student Enroll] --> B[Celery Queue]
    B --> C[send_enrollment_email]
    C --> D[Email Sent]
```

---

### 2. Certificate Generation Task

Task ini dijalankan ketika mahasiswa menyelesaikan course.

```mermaid
flowchart LR
    A[Complete Course] --> B[Celery Queue]
    B --> C[generate_certificate]
    C --> D[Certificate PDF]
```

---

### 3. Export Course Report Task

Task ini digunakan untuk membuat laporan peserta course dalam format CSV.

```mermaid
flowchart LR
    A[Teacher Request Report] --> B[Celery Queue]
    B --> C[export_course_report]
    C --> D[Generate CSV]
    D --> E[Email Notification]
```

---

### 4. Update Course Statistics Task

Task ini dijalankan secara berkala menggunakan Celery Beat.

```mermaid
flowchart LR
    A[Celery Beat Scheduler]
    A --> B[update_course_statistics]
    B --> C[Update Enrollment Count]
```

## MongoDB Collections

Bukti collection MongoDB berhasil dibuat.

![MongoDB Collections](docs/images/mongodb-collections.png)

Collection:

- activity_logs
- learning_analytics

---

## MongoDB Aggregation Query

Bukti aggregation query berhasil dijalankan.

![MongoDB Aggregation](docs/images/mongodb-aggregation.png)

---

## Flower Monitoring

Bukti seluruh Celery Task berhasil dijalankan.

![Flower Monitoring](docs/images/flower-success.png)

Task:

- send_enrollment_email
- generate_certificate
- export_course_report
- update_course_statistics

Status:

SUCCESS

---

## Certificate Generation

Bukti file PDF berhasil dibuat.

![Certificate](docs/images/certificate-generated.png)

File:

certificate_21_1_1781839120.pdf

---

## CSV Report

Bukti file CSV berhasil dibuat.

![CSV Report](docs/images/csv-report.png)

---

## RabbitMQ Dashboard

Bukti RabbitMQ berjalan.

![RabbitMQ](docs/images/rabbitmq-dashboard.png)

---

## Swagger Documentation

Bukti endpoint API tersedia.

![Swagger](docs/images/swagger-api.png)
