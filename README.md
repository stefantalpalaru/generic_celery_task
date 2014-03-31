##problem

The Celery daemon needs to be restarted every time an existing task is modified
or new tasks are added.

##solution

Use only one Celery task that's generic enough to run arbitrary Python
functions with arbitrary arguments and wrap this task in a custom decorator.

As a bonus, the job will still work (synchronously) when Celery/the broker are
not running.

The job's calling API is the same as Celery's: .s(), .delay() and
.apply\_async()

##example

- in celeryapp.py which is in the same directory as celeryconfig.py, create a
  Celery app and then import the custom decorator:

```python
import celery
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
app = celery.Celery()
app.config_from_object('celeryconfig')

from generic_celery_task.decorators import task

```

- start Celery along with its broker. You no longer need to restart Celery after this.

- in another file, importable from celeryapp.py, create your task:

```python
from celeryapp import task

@task
def job(x, y):
    return 'x + y = %d' % (x + y)
```

- now use it:

```python
import celery

# direct function call
assert job(1, 2) == 'x + y = 3'

# using the delay() method
res = job.delay(1, 2)
# if the Celery daemon and its backend broker are running, 'res' is an instance of AsyncResult
if isinstance(res, celery.result.AsyncResult):
    assert res.get() == 'x + y = 3'
else:
    # if either one is not running, a warning is issued and the function is executed synchronously
    # with 'res' being the actual function result
    # if you want to silence the warnings, use '@task(quiet=True)'
    assert res == 'x + y = 3'

# using the apply_async() method
res = job.apply_async(args=[1, 2])
# and process the result as above, if you need to
```

##installation

A setup.py is provided. You know what to do with it.

##testing

The tests require nose, redis, redis-py and assume that the port 6389 is free.

Run the tests with "python setup.py test" or with "nosetests -v".

This package was tested with python-2.7.6, python-3.3.4, nose-1.3.0,
celery-3.1.10, redis-2.8.7 and redis-py-2.9.1 .

##caveats

- the module which holds your custom task will be reloaded. If it contains a
  class using 'super' and its instance, you might run into the problem
  described [here][1]. Apply one of the proposed fixes.

- the state of the Celery daemon and its broker are checked only once, when the
  first .delay() or .apply\_async() method is called on a custom task.

##credits

- author: Stefan Talpalaru <stefantalpalaru@yahoo.com>

- homepage: https://github.com/stefantalpalaru/generic\_celery\_task


[1]: http://thingspython.wordpress.com/2010/09/27/another-super-wrinkle-raising-typeerror/

<!-- pandoc -o README.rst README.md -->

