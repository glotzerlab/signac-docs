# project.py
import signac

def compute_volume(job):
    volume = job.sp.N * job.sp.kT / job.sp.p
    with open(job.fn('volume.txt'), 'w') as file:
        file.write(str(volume) + '\n')

project = signac.get_project()
for job in project:
    compute_volume(job)
