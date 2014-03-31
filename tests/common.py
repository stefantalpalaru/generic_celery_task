import subprocess
import time
import os


redis_process = None
celery_process = None
DEVNULL = open(os.devnull, 'w')

def setup_redis():
    global redis_process
    if redis_process is not None:
        return
    redis_process = subprocess.Popen(['redis-server', '--port', '6389', '--bind', '127.0.0.1', '--logfile', ''], stdout=DEVNULL, stderr=DEVNULL)
    time.sleep(1)

def teardown_redis():
    global redis_process
    redis_process.terminate()
    timeout = 5 # seconds
    seconds_passed = 0
    start = time.time()
    while redis_process.poll() is None and seconds_passed < timeout:
        seconds_passed = time.time() - start
    if redis_process.poll() is None:
        redis_process.kill()
        redis_process.wait()
    redis_process = None

def setup_celery():
    global celery_process
    if celery_process is not None:
        return
    celery_process = subprocess.Popen(['celery', 'worker', '-A', 'celeryapp', '-Ofair'], stdout=DEVNULL, stderr=DEVNULL)
    time.sleep(2)

def teardown_celery():
    global celery_process
    celery_process.terminate()
    timeout = 5 # seconds
    seconds_passed = 0
    start = time.time()
    while celery_process.poll() is None and seconds_passed < timeout:
        seconds_passed = time.time() - start
    if celery_process.poll() is None:
        celery_process.kill()
        celery_process.wait()
    celery_process = None

