# Task Scheduler & Job Queue

A distributed task scheduler with a priority-based job queue, cron support, automatic retries, and worker threads.

## Stack

- **API** — FastAPI
- **Queue** — Redis (sorted by priority: high / medium / low)
- **Database** — PostgreSQL
- **Workers** — Python threads spawned per job

## How it works

1. A job is submitted via the REST API with a priority and optional scheduled time.
2. The job is persisted in Postgres and pushed onto the appropriate Redis queue.
3. The scheduler polls for queued jobs, marks them as `processing`, and spawns a worker thread.
4. The worker executes the job and logs the result. On failure, it retries up to 3 times before marking the job `failed`.
5. A timeout check runs each cycle — any job stuck in `processing` for over 30 minutes is re-queued.

## Setup

```bash
cp .env.example .env
docker compose up -d        # starts Postgres and Redis
psql -f db/schema.sql       # create tables
uvicorn api.app:app --reload
```

## API

| Method | Path | Description |
|---|---|---|
| `POST` | `/jobs` | Create and queue a job |
| `GET` | `/jobs/{job_id}` | Get job status |

**Job priorities:** `1` = high, `2` = medium, `3` = low

## Requirements

> These requirements were gathered during a mock system design interview. Only a subset has been implemented — the goal was to practice translating design decisions into working code, not to build a production system.

**Functional**
- Handle up to 10M jobs/day (~50k/min)
- Three priority levels: high, medium, low
- Support both one-time scheduled jobs and recurring cron jobs
- Each job has a persistent status (queued → processing → completed/failed)
- Max 3 retries per job before marking it failed
- Duplicate jobs (same payload) handled gracefully

**Non-functional**
- Queue availability > 99.99%
- Job pickup SLA: high < 1 min, medium < 5 min, low < 10 min
- Jobs running longer than 30 minutes are timed out and re-queued
- During traffic spikes, all jobs are queued and high priority is drained first
