import celery
import importlib
import warnings
try:
    from imp import reload
except:
    pass


class WorkerException(Exception):
    pass

class CeleryWorkersWarning(Warning):
    pass

class CeleryBrokerWarning(Warning):
    pass

# Checking this takes about a second so we only do it once.
WORKERS_ARE_RUNNING = None

@celery.shared_task
def generic_runner(mod_name, func_name, *args, **kwargs):
    """
    Turns out we can get around Celery's inability to add/modify tasks
    dynamically by using a single generic task.
    """
    mod = importlib.import_module(mod_name)
    reload(mod)
    return getattr(mod, func_name)(*args, **kwargs)

def task(*args, **kwargs):
    """
    Custom decorator to use the generic_runner task.  It overrides the 's', 'delay'
    and 'apply_async' methods from Celery's calling API in order to execute the
    task synchronously if we can't connect to the broker or if there are no
    workers running (for lazy developers that didn't bother setting up the
    Celery daemon locally ;-) ).

    !!! WARNING !!!
    If inside your task you are using objects from classes that use 'super' you're in for
    a nasty surprise due to module reloading:
    http://thingspython.wordpress.com/2010/09/27/another-super-wrinkle-raising-typeerror/

    This decorator does not support the options of the Celery decorator with the same name.
    Options supported:
        - 'quiet' - silence the output when the worker or the broker are not running. Defaults to False
    """
    def decorator(func):
        quiet = kwargs.get('quiet', False)

        def s(*args, **kwargs):
            return generic_runner.s(func.__module__, func.__name__, *args, **kwargs)
        func.s = s

        def _run(f, method, **opts):
            try:
                global WORKERS_ARE_RUNNING
                if WORKERS_ARE_RUNNING is None:
                    d = celery.task.control.inspect().stats()
                    if not d:
                        WORKERS_ARE_RUNNING = False
                    else:
                        WORKERS_ARE_RUNNING = True
                if not WORKERS_ARE_RUNNING:
                    raise WorkerException()
                res = getattr(f, method)(**opts)
            except WorkerException:
                if not quiet:
                    warnings.warn('Celery workers not running. Executing the task synchronously.', CeleryWorkersWarning, stacklevel=3)
                res = f()
            except Exception as e:
                if not quiet:
                    warnings.warn('Celery broker not running. Executing the task synchronously. (%s)' % e, CeleryBrokerWarning, stacklevel=3)
                res = f()
            return res

        def delay(*args, **kwargs):
            return _run(s(*args, **kwargs), 'delay')
        func.delay = delay

        def apply_async(args=None, kwargs=None, **opts):
            args = args or []
            kwargs = kwargs or {}
            return _run(s(*args, **kwargs), 'apply_async', **opts)
        func.apply_async = apply_async

        return func
    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator

