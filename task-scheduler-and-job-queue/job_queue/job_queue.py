from api.app import redis_client, PRIORITY_QUEUES

QUEUE_PRIORITY_MAP = {
    'queue:high': 1,
    'queue:medium': 2,
    'queue:low': 3
}

class JobQueue:

    @staticmethod
    def push(job_id: int, priority: int):
        PRIORITY_QUEUES = {1: 'queue:high', 2: 'queue:medium', 3: 'queue:low'}
        queue = PRIORITY_QUEUES.get(priority, 'queue:low')
        redis_client.lpush(queue, job_id)

    @staticmethod
    def pop():
        for queue_name in QUEUE_PRIORITY_MAP.keys():
            job_id = redis_client.lpop(queue_name)
            if job_id:
                return {
                    'job_id': int(job_id),
                    'priority': QUEUE_PRIORITY_MAP[queue_name]
                }
        return None  # all queues empty