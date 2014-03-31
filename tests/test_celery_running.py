from . import common
import warnings
from generic_celery_task.decorators import CeleryBrokerWarning
from generic_celery_task import decorators


def setup():
    common.setup_celery()
    global job2
    decorators.WORKERS_ARE_RUNNING = None
    from .jobs import job as job2

def teardown():
    common.teardown_celery()

def test_with_celery():
    res = job2(1, 2)
    assert res == 'x + y = 3'
    with warnings.catch_warnings(record=True) as w:
        try:
            warnings.simplefilter('ignore', ResourceWarning)
        except:
            pass
        res = job2.delay(1, 2)
        #print(w)
        #print(w[0].category)
        #print(w[0])
        #print(w[1].category)
        assert len(w) == 1
        assert issubclass(w[0].category, CeleryBrokerWarning)
        assert res == 'x + y = 3'
    with warnings.catch_warnings(record=True) as w:
        res = job2.apply_async(args=[1, 2])
        assert len(w) == 1
        assert issubclass(w[0].category, CeleryBrokerWarning)
        assert res == 'x + y = 3'

