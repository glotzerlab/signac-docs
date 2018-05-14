from signac import init_project

project = init_project('mpi-example-project')
for i in range(3):
    project.open_job(dict(foo=i)).init()

