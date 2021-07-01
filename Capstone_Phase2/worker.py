import os

import redis
from rq import Worker, Queue, Connection

conn = redis.Redis(
    # host=os.getenv("REDIS_HOST", "127.0.0.1"),
    host=os.getenv("REDIS_HOST", "redis"),
    port=os.getenv("REDIS_PORT", "6379"),
    password=os.getenv("REDIS_PASSWORD", ""),
)

listen = ['default']



# redis_url = os.getenv('REDISTOGO_URL', 'redis://redis:6379')

# conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()