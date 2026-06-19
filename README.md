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

## Redis Cache

Bukti Course List Cache dan Course Detail Cache.

![Redis Cache](docs/images/redis-cache.png)

Terlihat key cache:

- simple_lms:1:courses:list:...
- simple_lms:1:course:1

---

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
