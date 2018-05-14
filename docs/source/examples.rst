.. _examples:

========
Examples
========

Ideal Gas
=========

This example is based on the :ref:`tutorial` and assumes that we want to model a system using the ideal gas law:

.. math::

    p V = N k_B T

The data space is initialized for a specific system size :math:`N`, thermal energy :math:`kT`, and pressure :math:`p` in a script called ``init.py``:

.. code-block:: python

    # init.py
    import signac

    project = signac.init_project('ideal-gas-project')

    for p in range(1, 11):
        sp = {'p': p, 'kT': 1.0, 'N': 1000}
        job = project.open_job(sp)
        job.init()

The workflow consists of a ``compute_volume`` operation, that computes the volume based on the given parameters and stores it within a file called ``V.txt`` within each job's workspace directory.
The two additional operations copy the result into a JSON file called ``data.json`` and into the job document under the ``volume`` key respectively.
All operations are defined in ``project.py``:

.. code-block:: python

    # project.py
    from flow import FlowProject


    @FlowProject.label
    def volume_computed(job):
        return job.isfile("volume.txt")


    @FlowProject.operation
    @FlowProject.post.isfile("volume.txt")
    def compute_volume(job):
        volume = job.sp.N * job.sp.kT / job.sp.p
        with open(job.fn("volume.txt"), "w") as file:
            file.write(str(volume) + "\n")


    @FlowProject.operation
    @FlowProject.pre.after(compute_volume)
    @FlowProject.post.isfile("data.json")
    def store_volume_in_json_file(job):
        import json
        with open(job.fn("volume.txt")) as textfile:
            with open(job.fn("data.json"), "w") as jsonfile:
                data = {"volume": float(textfile.read())}
                jsonfile.write(json.dumps(data) + "\n")


    @FlowProject.operation
    @FlowProject.pre.after(compute_volume)
    @FlowProject.post(lambda job: 'volume' in job.document)
    def store_volume_in_document(job):
        with open(job.fn("volume.txt")) as textfile:
            job.document.volume = float(textfile.read())


    if __name__ == '__main__':
        FlowProject().main()

The complete workflow can be executed on the command line with ``$ python project.py run``.


Pumpkin cannon
==============

HPMC with HOOMD-blue
====================

MD with GROMACS
===============
