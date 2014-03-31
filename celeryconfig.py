BROKER_URL = 'redis://localhost:6389/1' # the standard port is 6379. we use 6389 for testing
CELERY_RESULT_BACKEND = 'redis://localhost:6389/1'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 36000}  # 10 hours
BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True

