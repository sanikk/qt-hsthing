from invoke import task


@task
def start(c):
    c.run('python qt-HSthing/main.py')
