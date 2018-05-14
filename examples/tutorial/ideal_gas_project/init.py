# init.py
import signac

project = signac.init_project('ideal-gas-project')

for p in range(1, 11):
    sp = {'p': p, 'kT': 1.0, 'N': 1000}
    job = project.open_job(sp)
    job.init()
