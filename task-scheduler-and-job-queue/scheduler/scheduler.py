import threading
from worker import Worker
import time
from api.app import get_db
from queue.job_queue import JobQueue

class Scheduler:

    @staticmethod
    def pick_next_job(conn):
        sql_query = '''SELECT id, task_id, params, priority, retry_count, max_retries 
            FROM jobs 
            WHERE status = 'queued' 
            AND scheduled_at <= NOW()
            ORDER BY priority ASC, scheduled_at ASC
            FOR UPDATE SKIP LOCKED
            LIMIT 1'''
        cursor = conn.cursor()
        cursor.execute(sql_query)
        job = cursor.fetchone()
        return job

    @staticmethod
    def mark_processing(conn, job_id):
        cursor = conn.cursor()
        sql_query = '''UPDATE jobs SET status='processing', updated_at = NOW() WHERE id=%s'''
        cursor.execute(sql_query, (job_id,))
        conn.commit()

    @staticmethod
    def spawn_worker(job):
        thread = threading.Thread(target=Worker.execute, args=(job,))
        thread.start()
        return thread

    @staticmethod
    def check_timeouts():
        conn = next(get_db())
        cursor = conn.cursor()
        timeout_sql = '''SELECT * FROM jobs WHERE updated_at < NOW() - INTERVAL '30 minutes' AND status = 'processing' '''
        cursor.execute(timeout_sql)
        jobs = cursor.fetchall()
        for job in jobs:
            JobQueue.push(job[0], job[3])

    def run():
        while True:
            conn = next(get_db())
            job = Scheduler.pick_next_job(conn)
            if not job:
                print('No job for processing')
                time.sleep(5)
                continue
            Scheduler.mark_processing(conn, job[0])
            Scheduler.spawn_worker(job)
            Scheduler.check_timeouts()
            time.sleep(5)