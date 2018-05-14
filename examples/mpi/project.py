from flow import FlowProject, cmd, directives


# MPI-parallelized operation using mpi4py:
# Execute directly with:
# $ mpiexec -n 2 python project.py exec mpi_hello_world
# or
# $ mpiexec -n 2 python project.py run -o mpi_hello_world
# To generate scripts you would need to take one of the two
# approaches shown below.
@FlowProject.operation
def mpi_hello_world(job):
    from mpi4py import MPI
    print("Hello from rank:", MPI.COMM_WORLD.Get_rank())


# This cmd-operaiton calls another MPI program, which may
# be our own script or any other program.
# Execute this operation with:
# $ python project.py exec mpi_hello_world_cmd
# or
# $ python project.py run -o mpi_hello_world
#
# Providing the number of processors (np) with the @directives
# decorator is not strictly necessary, but might be used by some
# script templates to either directly prepend the command with
# mpiexec or equivalent, and/or to calculate required resources.
@FlowProject.operation
@directives(np=2)
@cmd
def mpi_hello_world_cmd(job):
    return "mpiexec -n 2 python project.py exec mpi_hello_world {job._id}"
    # Or any other program:
    # return "mpiexec -n 2 ./mpi_hello_world"


# The np argument to the directives operator can be a function of job:
@FlowProject.operation
@directives(np=lambda job: job.sp.foo+1)
def mpi_hello_world_dynamic_np(job):
    from mpi4py import MPI
    print("Hello from rank:", MPI.COMM_WORLD.Get_rank())


if __name__ == '__main__':
    FlowProject().main()
