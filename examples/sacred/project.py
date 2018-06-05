from flow import FlowProject
from sacred.observers import FileStorageObserver

from experiment import ex


class SacredProject(FlowProject):
    pass


@SacredProject.operation
def run_experiment(job):
    ex.add_config(** job.sp())
    ex.observers[:] = [FileStorageObserver.create(job.fn('my_runs'))]
    ex.run()


if __name__ == '__main__':
    SacredProject().main()
