# init.py
import signac

project = signac.init_project('my-project')

for foo in range(9):
    for bar in True, False:
        job = project.open_job(dict(foo=foo, bar=bar))
        job.init()
