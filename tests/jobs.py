from celeryapp import task

@task
def job(x, y):
    return 'x + y = %d' % (x + y)

@task(quiet=True)
def quiet_job(x, y):
    return 'x + y = %d' % (x + y)

