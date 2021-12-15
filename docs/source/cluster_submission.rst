.. _cluster-submission:

==================
Cluster Submission
==================

While it is always possible to manually write and submit scripts to a cluster, using the *flow interface* to generate and submit scripts on our behalf will allow **signac-flow** to **keep track of submitted operations** and prevent the resubmission of active operations.

In addition, **signac-flow** uses :ref:`environment profiles <environments>` to select which :ref:`base template <templates>` to use for the cluster job script generation.
All base templates are in essence highly similar, but are adapted for a specific cluster environment.
This is necessary, because different cluster environments offer different resources and use slightly different ways to specify these resources.
You can check out the available options for the currently active environment with the ``python project.py submit --help`` command.

The *submit* interface
======================

In general, we submit operations through the primary interface of the :py:class:`~.flow.FlowProject`.
We assume that we use the same ``project.py`` module as shown in the previous section.

Then we can submit operations from the command line with the following command:

.. code-block:: bash

      ~/my_project $ python project.py submit

This will submit all *eligible* job-operations to the cluster scheduler and block that specific job-operation from resubmission.

In some cases you can provide additional arguments to the scheduler, such as which partition to submit to, which will then be used by the template script.
In addition you can always forward any arguments directly to the scheduler as positional arguments.
For example, if we wanted to specify an account name with a *PBS* scheduler, we could use the following command:

.. code-block:: bash

      ~/my_project $ python project.py submit -- -l A:my_account_name

Everything after the two dashes ``--`` will not be interpreted by the *submit* interface, but directly forwarded to the scheduler *as is*.

.. warning::

    **signac-flow** relies on the scheduler job name to recognize the status of submitted jobs.
    Users should not override the job name manually via the command line or a custom template.

Unless you have one of the :ref:`supported schedulers <environments>` installed, you will not be able to submit any operations in your local environment.
However, **signac-flow** comes with a simple scheduler for testing purposes.
You can execute it with ``$ simple-scheduler run`` and then follow the instructions on screen.

Submitting specific Operations
==============================

The submission process consists of the following steps:

  1. *Gathering* of all job-operations *eligible* for submission.
  2. Generation of scripts to execute those job-operations.
  3. Submission of those scripts to the scheduler.

The first step is largely determined by your project *workflow*.
You can see which operation might be submitted by looking at the output of ``$ python project.py status --detailed``.
You may further reduce the operations to be submitted by selecting specific jobs (*e.g.* with the ``-j``, ``-f``, or ``-d`` options), specific operations (``-o``), or generally reduce the total number of operations to be submitted (``-n``).
For example the following command would submit up to 5 ``hello`` operations, where *the state point key a is less than 5*.

.. code-block:: bash

    ~/my_project $ python project.py submit -o hello -n 5 -f a.\$lt 5

.. tip::

    Use the ``--pretend`` option to preview the generated submission scripts on screen instead of submitting them.


Bundling
========

By default, all eligible job-operations will be submitted as separate cluster jobs.
This is usually the best model for clusters that provide shared compute partitions because it allows the cluster scheduler to optimize the scheduling of your job.
However, sometimes it is beneficial to execute multiple operations within one cluster job, like if the compute cluster can only make reservation for full nodes or if there is a limit to the number of cluster jobs you can submit to the cluster scheduler's queue.

You can execute multiple job-operations in serial per cluster job submission with the ``--bundle`` option.
For example, the following command will bundle up to five job-operations to be executed in each cluster submission:

.. code-block:: bash

    ~/my_project $ python project.py submit --bundle=5

Without any argument, the ``--bundle`` option will bundle **all** eligible job-operations into a single cluster job.

.. tip::

    Recognizing that ``--bundle=1`` is the default option might help you to better understand the bundling concept.

By default, the submit command will run bundled job-operations in serial.
It is possible to run multiple CPU processes in parallel, as long as the operating system assigns running threads to any available CPU cores, which is not the default behavior on all compute clusters.
The ``--parallel`` flag will start the bundled job-operations and run them as background processes. Ensure that the processes are correctly assigned to the requested resources before using this option.

.. warning::

    The ``--parallel`` option will not distribute operations among multiple GPUs. Use aggregation instead. (TODO: link to tutorial)
    To distribute across multiple GPUs, clusters may require a split MPI communicator.
    An example of this behavior can be found in the `signac-examples project flow.aggregation-mpi <https://github.com/glotzerlab/signac-examples/tree/master/projects/flow.aggregation-mpi>`__.

.. _cluster_submission_directives:

Submission Directives
=====================

Executing operations on a cluster environment may involve the specification of resources that are required for said operation
For this, any :py:class:`~flow.FlowProject` *operation* can be amended with so called *submission directives*.
For example, to specify that a parallelized operation requires **4** processing units, we would provide the ``np=4`` directive:

.. code-block:: python

    from flow import FlowProject
    from multiprocessing import Pool

    @FlowProject.operation.with_directives({"np": 4})
    def hello(job):
        with Pool(4) as pool:
          print("hello", job)

.. note::

    The directive *np=4* means that the operation **requires** 4 processing units, the operation is not automatically parallelized.

All directives are essentially conventions, the ``np`` directive in particular means that this particular operation requires 4 processors for execution.

.. tip::

    Note that all directives may be specified as callables, e.g. ``FlowProject.operation.with_directives({"np": lambda job: job.doc.np})``.

Available directives
--------------------

The following directives are respected by all base templates shipped with **signac-flow**:

.. glossary::

    executable
      Specify which Python executable should be used to execute this operation.
      Defaults to the one used to generate the script (:py:attr:`sys.executable`).

    fork
      The fork directive can be set to True to enforce that a particular operation is always executed within a subprocess and not within the Python interpreter's process even if there are no other reasons that would prevent that.

    memory
      The memory to request for this operation.

    ngpu
      The number of GPUs required for this operation.

    np
      The total number of processing units required for this operation.
      The default value for np is "nranks x omp_num_threads", which both default to 1.

    nranks
      The number of MPI ranks required for this operation.
      The command will be prefixed with environment specific MPI command, e.g.: ``mpiexec -n 4``.

    omp_num_threads
      The number of OpenMP threads required for this operation.

    processor_fraction
      Fraction of a resource to use on a single operation.

    walltime
      The number of hours to request for executing this job.

For more detailed information about supported directives, visit the API reference doc of `directives <https://docs.signac.io/projects/flow/en/latest/api.html#flow.directives>`_.

Execution Modes
---------------

Using these directives and their combinations allows us to realize the following essential execution modes:

.. glossary::

    serial:
      ``@FlowProject.operation.with_directives()``

      This operation is a simple serial process, no directive needed.

    parallelized:
      ``@FlowProject.operation.with_directives({"np": 4})``

      This operation requires 4 processing units.

    MPI parallelized:
      ``@FlowProject.operation.with_directives({"nranks": 4})``

      This operation requires 4 MPI ranks.

    MPI/OpenMP Hybrid:
      ``@FlowProject.operation.with_directives({"nranks": 4, "omp_num_threads": 2})``

      This operation requires 4 MPI ranks with 2 OpenMP threads per rank.

    GPU:
      ``@FlowProject.operation.with_directives({"ngpu": 1})``

      The operation requires one GPU for execution.

The :ref:`next section <environments>` provides more details on how to select and define custom environments.
