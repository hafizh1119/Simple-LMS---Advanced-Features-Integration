# Caching Strategy - Redis

## Endpoint yang Di-cache

| Endpoint                  | Key Pattern           | TTL     |
| ------------------------- | --------------------- | ------- |
| `GET /api/courses-cached` | `courses:list:{hash}` | 5 menit |

## Alur Caching

```mermaid
sequenceDiagram
    participant Client
    participant API as Django API
    participant Redis as Redis Cache
    participant DB as PostgreSQL

    Client->>API: GET /api/courses-cached?search=python
    API->>API: Generate cache key dari parameter search
    API->>Redis: Cek key: courses:list:{hash}

    alt Cache Hit (Data ditemukan)
        Redis-->>API: Kembalikan data dari cache
        API-->>Client: Response dalam <10ms
        Note over Client,API: 97% lebih cepat dari tanpa cache
    else Cache Miss (Data tidak ada)
        Redis-->>API: Cache kosong
        API->>DB: SELECT * FROM courses WHERE name ILIKE '%python%'
        DB-->>API: Hasil query (150ms)
        API->>Redis: Simpan hasil ke cache dengan TTL 5 menit
        API-->>Client: Response
        Note over Client,API: Data disimpan untuk request berikutnya
    end
```
