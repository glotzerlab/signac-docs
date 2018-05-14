# project.py
from flow import FlowProject

@FlowProject.operation
def hello_job(job):
    print("Hello from job {}, my foo is '{}'.".format(job, job.sp.foo))


if __name__ == '__main__':
    FlowProject().main()
