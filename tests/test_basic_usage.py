from celeryapp import task
from generic_celery_task.decorators import CeleryBrokerWarning
from generic_celery_task import decorators
import warnings


def setup():
    global job4, quiet_job4
    decorators.WORKERS_ARE_RUNNING = None
    from .jobs import job as job4, quiet_job as quiet_job4

def test_direct_calls():
    assert job4(1, 2) == 'x + y = 3'
    assert quiet_job4(1, 2) == 'x + y = 3'

def test_delay():
    with warnings.catch_warnings(record=True) as w:
        res = job4.delay(1, 2)
        assert len(w) == 1
        assert issubclass(w[0].category, CeleryBrokerWarning)
        assert res == 'x + y = 3'
    with warnings.catch_warnings(record=True) as w:
        res = quiet_job4.delay(1, 2)
        assert len(w) == 0
        assert res == 'x + y = 3'

def test_apply_async():
    with warnings.catch_warnings(record=True) as w:
        res = job4.apply_async(args=[1, 2])
        assert len(w) == 1
        assert issubclass(w[0].category, CeleryBrokerWarning)
        assert res == 'x + y = 3'
    with warnings.catch_warnings(record=True) as w:
        res = quiet_job4.apply_async(args=[1, 2])
        assert len(w) == 0
        assert res == 'x + y = 3'

