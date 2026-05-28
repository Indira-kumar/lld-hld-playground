import json
import os
from typing import Optional
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from datetime import datetime
from psycopg2 import pool
import redis


# settings
class Settings(BaseSettings):
    app_name: str = "Task Scheduler API"
    db_host: str = os.getenv('DB_HOST', 'localhost')
    db_port: int = os.getenv('DB_PORT', 6300)
    db_name: str = os.getenv('DB_NAME', 'task_scheduler')
    db_user: str = os.getenv('DB_USER', 'postgres')
    db_password: str = os.getenv('DB_PASSWORD', 'postgres')
    redis_host: str = os.getenv('REDIS_HOST', 'localhost')
    redis_port: int = os.getenv('REDIS_PORT', 6301)

settings = Settings()


# models
class JobCreateRequest(BaseModel):
    cron_id: Optional[int]
    task_id: int
    params: Optional[object] = {}
    priority: Optional[int] = 0,
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now() 
    scheduled_at: Optional[datetime]


# DB connection setup
db_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=settings.db_host,
    port=settings.db_port,
    dbname=settings.db_name,
    user=settings.db_user,
    password=settings.db_password
)
def get_db():
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)


# redis connection
redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port)
PRIORITY_QUEUES = {1: 'queue:high', 2: 'queue:medium', 3: 'queue:low'}


# fast api app
app = FastAPI(title=settings.app_name)


# routes
job_router = APIRouter(prefix='/jobs')


# services
@job_router.get('/{job_id}')
async def read_job(job_id:int, conn=Depends(get_db)):
    cursor = conn.cursor()
    get_job_by_id_sql = f'SELECT * from jobs where id={job_id}'
    cursor.execute(get_job_by_id_sql)
    job = cursor.fetchone()
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')
    return job

@job_router.post('/')
async def create_job(job: JobCreateRequest, conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO jobs (cron_id, task_id, status, params, priority, scheduled_at, created_at, updated_at)
           VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
           RETURNING id''',
        (job.cron_id, job.task_id, 'queued', json.dumps(job.params), job.priority, job.scheduled_at)
    )
    job_id = cur.fetchone()[0]
    conn.commit()

    queue_name = PRIORITY_QUEUES.get(job.priority, 'queue:low')
    redis_client.lpush(queue_name, job_id)

    return {'job_id': job_id, 'status': 'queued'}


app.include_router(job_router)
