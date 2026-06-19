# Caching Strategy - Redis

## Endpoint yang Di-cache

| Endpoint | Key Pattern | TTL |
|----------|------------|-----|
| GET /api/courses-cached | courses:list:{hash} | 5 menit |
| GET /api/courses/{id} | course:{id} | 5 menit |

## Alur Caching
mermaid
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

## Cache Invalidation Strategy
mermaid
flowchart LR
    A[Create Course] --> B[Delete Course List Cache]
    C[Update Course] --> D[Delete Course List Cache]
    C --> E[Delete Course Detail Cache]
    F[Delete Course] --> G[Delete Course List Cache]
    F --> H[Delete Course Detail Cache]
