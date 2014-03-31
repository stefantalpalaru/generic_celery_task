from . import common
import warnings
from generic_celery_task.decorators import CeleryWorkersWarning
from generic_celery_task import decorators


def setup():
    common.setup_redis()
    global job1
    decorators.WORKERS_ARE_RUNNING = None
    from .jobs import job as job1

def teardown():
    common.teardown_redis()

def test_with_redis():
    res = job1(1, 2)
    assert res == 'x + y = 3'
    with warnings.catch_warnings(record=True) as w:
        try:
            warnings.simplefilter('ignore', ResourceWarning)
        except:
            pass
        res = job1.delay(1, 2)
        assert len(w) == 1
        assert issubclass(w[0].category, CeleryWorkersWarning)
        assert res == 'x + y = 3'
    with warnings.catch_warnings(record=True) as w:
        res = job1.apply_async(args=[1, 2])
        assert len(w) == 1
        assert issubclass(w[0].category, CeleryWorkersWarning)
        assert res == 'x + y = 3'

