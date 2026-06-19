# Architecture Diagram

Diagram arsitektur sistem yang menunjukkan integrasi Django API, PostgreSQL, Redis, MongoDB, Celery, RabbitMQ, dan Flower.

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

---

# Docker Services

Screenshot berikut menunjukkan seluruh service Docker berhasil berjalan.

**Screenshot:** `docker ps`

![Docker Services](docs/images/docker-services.png)

Container yang aktif:

* lms-app
* lms-db
* lms-redis
* lms-mongodb
* lms-rabbitmq
* lms-celery-worker
* lms-celery-beat
* lms-flower

---

# API Documentation

Screenshot berikut menunjukkan dokumentasi API berhasil digenerate menggunakan Swagger.

**Screenshot:** `http://localhost:8000/api/docs`

![Swagger API](docs/images/swagger-api.png)

Endpoint yang tersedia:

* Authentication
* Course Management
* Enrollment
* Progress Tracking
* Async Processing

---

# Caching Strategy - Redis

Sistem menggunakan Redis sebagai caching layer untuk meningkatkan performa API dan mengurangi query langsung ke PostgreSQL.

### Endpoint yang Di-cache

| Endpoint                | Key Pattern         | TTL     |
| ----------------------- | ------------------- | ------- |
| GET /api/courses-cached | courses:list:{hash} | 5 menit |
| GET /api/courses/{id}   | course:{id}         | 5 menit |

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

```mermaid
flowchart LR
    A[Create Course] --> B[Delete Course List Cache]
    C[Update Course] --> D[Delete Course List Cache]
    C --> E[Delete Course Detail Cache]
    F[Delete Course] --> G[Delete Course List Cache]
    F --> H[Delete Course Detail Cache]
```

---

# Redis Cache

Screenshot berikut menunjukkan key cache berhasil tersimpan di Redis.

**Screenshot:** `redis-cli -> KEYS *`

![Redis Cache](docs/images/redis-cache.png)

Key yang berhasil dibuat:

* simple_lms:1:courses:list:...
* simple_lms:1:course:1

---

# Rate Limiting

Screenshot berikut menunjukkan implementasi Redis Rate Limiting.

**Screenshot:** `lms/throttle.py`

![Rate Limiting](docs/images/rate-limiting.png)

Konfigurasi:

* Rate Limit : 60 Request / Minute
* Menggunakan Redis sebagai penyimpanan counter request.

---

# Task Flow Documentation

### Enrollment Email Task

```mermaid
flowchart LR
    A[Student Enroll] --> B[Celery Queue]
    B --> C[send_enrollment_email]
    C --> D[Email Sent]
```

### Certificate Generation Task

```mermaid
flowchart LR
    A[Complete Course] --> B[Celery Queue]
    B --> C[generate_certificate]
    C --> D[Certificate PDF]
```

### Export Course Report Task

```mermaid
flowchart LR
    A[Teacher Request Report] --> B[Celery Queue]
    B --> C[export_course_report]
    C --> D[Generate CSV]
    D --> E[Email Notification]
```

### Update Course Statistics Task

```mermaid
flowchart LR
    A[Celery Beat Scheduler]
    A --> B[update_course_statistics]
    B --> C[Update Enrollment Count]
```

---

# MongoDB Collections

Screenshot berikut menunjukkan collection MongoDB berhasil dibuat.

**Screenshot:** `show collections`

![MongoDB Collections](docs/images/mongodb-collections.png)

Collection:

* activity_logs
* learning_analytics

---

# Activity Logs

Screenshot berikut menunjukkan aktivitas pengguna berhasil dicatat ke MongoDB.

**Screenshot:** `db.activity_logs.find().limit(5).pretty()`

![Activity Logs](docs/images/activity-logs.png)

Aktivitas yang tercatat:

* list_cached
* enroll_async
* complete_course

---

# Learning Analytics

Screenshot berikut menunjukkan data analytics pembelajaran tersimpan di MongoDB.

**Screenshot:** `db.learning_analytics.find().limit(5).pretty()`

![Learning Analytics](docs/images/learning-analytics.png)

Data yang tersimpan:

* user_id
* course_id
* event_type
* timestamp

---

# Aggregation Query

Screenshot berikut menunjukkan query agregasi MongoDB berhasil dijalankan.

**Screenshot:** `db.learning_analytics.aggregate(...)`

![MongoDB Aggregation](docs/images/mongodb-aggregation.png)

Tujuan:

* Menghitung total view per course
* Menentukan course yang paling populer

---

# Flower Monitoring

Screenshot berikut menunjukkan seluruh task Celery berhasil dijalankan.

![Flower Monitoring](docs/images/flower-success.png)

Task yang berhasil dieksekusi:

* send_enrollment_email
* generate_certificate
* export_course_report
* update_course_statistics

Status: SUCCESS

---

# RabbitMQ Dashboard

Screenshot berikut menunjukkan RabbitMQ Management Dashboard berhasil berjalan.

![RabbitMQ Dashboard](docs/images/rabbitmq-dashboard.png)

Fungsi:

* Message Broker
* Queue Management
* Monitoring Queue

---

# Certificate Generation

Screenshot berikut menunjukkan file sertifikat PDF berhasil dibuat.

![Certificate Generation](docs/images/certificate-generated.png)

File:

* certificate_21_1_1781839120.pdf

---

# CSV Report Generation

Screenshot berikut menunjukkan file laporan CSV berhasil dibuat.

![CSV Report](docs/images/csv-report.png)

File:

* report_course_54_1781840103.csv

---

# Testing Results

| Fitur                  | Status  |
| ---------------------- | ------- |
| Redis Cache            | SUCCESS |
| Rate Limiting          | SUCCESS |
| MongoDB Logging        | SUCCESS |
| Learning Analytics     | SUCCESS |
| Aggregation Query      | SUCCESS |
| Celery Tasks           | SUCCESS |
| RabbitMQ               | SUCCESS |
| Flower Monitoring      | SUCCESS |
| Certificate Generation | SUCCESS |
| CSV Report Export      | SUCCESS |

---

# Conclusion

Seluruh fitur Advanced Features Integration berhasil diimplementasikan dan diuji menggunakan Redis, MongoDB, Celery, RabbitMQ, Flower, PostgreSQL, dan Docker. Seluruh requirement tugas berhasil dipenuhi dan berjalan dengan baik.
