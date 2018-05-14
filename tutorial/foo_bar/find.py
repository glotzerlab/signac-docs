import signac

project = signac.get_project()
for job in project.find_jobs({"bar": True}):
    print(job, job.sp.foo)
