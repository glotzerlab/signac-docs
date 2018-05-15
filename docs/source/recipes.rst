.. _recipes:

=======
Recipes
=======

This is a collection of recipes on how to solve typical problems using **signac**.

.. todo::

    Move all recipes below into a 'General' section once we have added more recipes.

How to migrate (change) the data space schema.
==============================================

Oftentimes, one discovers at a later stage that important keys are missing from the metadata schema.
For example, in the tutorial we are modeling a gas using the ideal gas law, but we might discover later that important effects are not captured using this overly simplistic model and decide to replace it with the van der Waals equation:

.. math::

   \left(p + \frac{N^2 a}{V^2}\right) \left(V - Nb \right) = N k_B T

Since the ideal gas law can be considered a special case of the equation above with :math:`a=b=0`, we could migrate all jobs with:

.. code-block:: python

    >>> for job in project:
    ...     job.sp.setdefault('a', 0)
    ...     job.sp.setdefault('b', 0)
    ...

The ``setdefault()`` function sets the value for :math:`a` and :math:`b` to 0 in case that they are not already present.
To *delete* a key use ``del job.sp['key_to_be_removed']``.
To *rename* a key, use ``job.sp.new_name = job.sp.pop('old_name')``.

.. note::

    The ``job.sp`` attribute provides all basic functions  of a regular Python dict.


How to integrate signac-flow with matlab or other software without Python interface
===================================================================================

The easiest way to integrate software that has no native Python interface is to implement ``signac-flow`` operations in combination with the ``flow.cmd`` decorator.
Assuming that we have a matlab script called ``prog.m`` within the project root directory:

.. code-block:: matlab

    % prog.m
    function []=prog(arg1, arg2)

    display(arg1);
    display(arg2);

    exitcode = 0;

Then, we could impement a simple operation that passes it some metadata parameters like this:

.. code-block:: python

    @FlowProject.operation
    @flow.cmd
    def compute_volume(job):
        return "matlab -r 'prog {job.sp.foo} {job.sp.bar}' > {job.ws}/output.txt"

Executing this operation will store the output of the matlab script within the job's workspace within a file called ``output.txt``.

How to implement MPI-parallelized operations
============================================

There are basically two strategies to implement :class:`~.flow.FlowProject` operations that are MPI-parallelized, one for external programs and one for Python scripts.

.. tip::

    Fully functional scripts can be found in the signac-docs repository under ``examples/MPI``.


MPI-operations with mpi4py or similar
-------------------------------------

Assuming that your operation is using mpi4py or similar, you don't really have to change anything to the code:

.. code-block:: python

    @FlowProject.operation
    def hello_mpi(job):
        from mpi4py import MPI
        print("Hello from rank", MPI.COMM_WORLD.Get_rank())

You could run this operation directly with: ``mpiexec -n 2 python project.py run -o hello_mpi``.

.. note::

    This strategy might fail in cases where you cannot ensure that the MPI communicator is initialized *within* the operation function.

MPI-operations with ``flow.cmd``
--------------------------------

Alternatively, you can implement an MPI-parallelized operation with the ``flow.cmd`` decorator, optionally in combination with the ``flow.directives`` decorator.
This strategy lets you define the number of ranks directly within the code and is also the only possible strategy when integrating external programs without a Python interface.

Assuming that we have an MPI-parallelized program named ``my_programm``, which expects an input file as its first argument and which we want to run on two ranks, we could implement the operation like this:

.. code-block:: python

    @FlowProject.operation
    @flow.cmd
    @flow.directives(np=2)
    def hello_mpi(job):
        return "mpiexec -n 2 mpi_program {job.ws}/input_file.txt"

The ``flow.cmd`` decorator instructs signac-flow to interpret the operation as a command rather than a Python function.
The ``flow.directives`` decorator provides additional instructions on how to execute this operation and is not strictly necessary for the example above to work.
However, some script templates, including those designed for HPC cluster submissions, will use the value provided by the ``np`` key to compute the required compute ranks for a specific submission.

.. tip::

  You do not have to *hard-code* the number of ranks, it may be a function of the job, *e.g.*: ``flow.directives(np=lambda job: job.sp.system_size // 1000)``.


MPI-operations with custom script templates
-------------------------------------------

Finally, instead of modifying the operation implementation, you could use a custom script template, such as this one:

.. code-block:: bash

    {% extends base_script %}
    {% block body %}
    {% for operation in operations %}
    mpiexec -n {{ operation.directives.np }} operation.cmd
    {% endfor %}
    {% endblock %}

Storing the above template in a file called ``templates/script.sh`` within your project root directory will prepend *every* operation command with ``mpiexec`` and so on.

.. todo::

    Advanced Workflows

      1. How to do hyperparameter optimization for your awesome ML application.
      2. How to implement branched workflows.
      3. How to implement a dynamic data space (*e.g.* add jobs on-the-fly).
      4. How to implement aggregation operations.

    Parallel and Super Computing

      1. How to run and submit MPI operations.
      2. How to adjust your submit script header.
      3. How to submit a bundle of operations to a cluster.
      4. How to synchronize between two different compute environments.
      5. How to use **signac** in combination with a docker/singularity container.
