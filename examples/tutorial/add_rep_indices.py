# init.py
import signac

project = signac.init_project('ideal-gas-project')
num_reps = 3

jobs = project.find_jobs({"replica_index.$exists":False})
for job in jobs:
    job.sp['replica_index']=0

for i in range(num_reps) :
    for p in range(1, 11):
        sp = {'p': p, 'kT': 1.0, 'N': 1000, "replica_index": i}
        job = project.open_job(sp)
        if(job not in project):
            job.init()
