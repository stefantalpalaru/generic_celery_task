from . import common
import warnings
from generic_celery_task import decorators
import celery


def setup():
    common.setup_redis()
    common.setup_celery()
    global job3
    decorators.WORKERS_ARE_RUNNING = None
    from .jobs import job as job3

def teardown():
    common.teardown_celery()
    common.teardown_redis()

def test_with_both():
    res = job3(1, 2)
    assert res == 'x + y = 3'
    with warnings.catch_warnings(record=True) as w:
        res = job3.delay(1, 2)
        assert len(w) == 0
        assert isinstance(res, celery.result.AsyncResult)
        assert res.get() == 'x + y = 3'
    with warnings.catch_warnings(record=True) as w:
        res = job3.apply_async(args=[1, 2])
        assert len(w) == 0
        assert isinstance(res, celery.result.AsyncResult)
        assert res.get() == 'x + y = 3'

