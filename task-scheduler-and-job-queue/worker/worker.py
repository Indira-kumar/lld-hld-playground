from api.app import get_db
from queue.job_queue import JobQueue
import datetime
import time
import threading

class Worker:
    @staticmethod
    def execute(job):
        conn = next(get_db())
        try:
            cursor = conn.cursor()
            started = datetime.datetime.now()
            time.sleep(2)

            completed_job_params = (job[0], threading.current_thread().name, started)
            completed_query = '''INSERT INTO job_logs (job_id, worker_id, status, started_at, completed_at)
                VALUES (%s, %s, 'completed', %s, NOW())'''
            cursor.execute(completed_query, completed_job_params)
            conn.commit()
        except Exception as e:
            print("Error executing job: %s", e)
            Worker.handle_failure(conn, job)

    @staticmethod
    def handle_failure(conn, job):
        cursor = conn.cursor()
        get_job_sql = '''SELECT * FROM jobs where id=%s'''
        job_params = (job[0],)
        cursor.execute(get_job_sql, job_params)
        jobs = cursor.fetchone()
        if jobs[4] < jobs[5]:
            retry_count = jobs[4] + 1
            update_sql = '''UPDATE jobs SET status='queued', retry_count = %s WHERE id=%s'''
            cursor.execute(update_sql, (retry_count, job[0]))
            JobQueue.push(job[0], job[3])
            conn.commit()
        else:
            update_sql = '''UPDATE jobs SET status='failed' WHERE id=%s'''
            cursor.execute(update_sql, (job[0],))
            conn.commit()