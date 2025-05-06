.. _tutorial:

========
Tutorial
========

.. sidebar:: License

    The code shown in this tutorial is part of the :ref:`examples`.
    It can be downloaded from the signac-docs_ repository and is released into the `public domain <https://github.com/glotzerlab/signac-docs/blob/main/examples/LICENSE.txt>`_.

.. _signac-docs: https://github.com/glotzerlab/signac-docs

This tutorial is designed to step new users through the basics of setting up a **signac** data space, defining and executing a simple workflow with **signac-flow**, and analyzing the data.

Basics
======


Initializing the data space
---------------------------

In this tutorial, we will perform a simple study of the pressure-volume (*p-V*) relationship of a noble gas.
As a first approximation, we could model the gas as an *ideal gas*, so the *ideal gas law* applies:

.. math::

    p V = N k_B T

Therefore, we can assume that the volume :math:`V` can be directly calculated as a function of system size :math:`N`, Boltzmann's constant :math:`k_B`, and temperature :math:`T`.

To test this relationship, we start by creating an empty project directory where we will place all the code and data associated with this computational study.

.. code:: bash

    ~ $ mkdir ideal_gas_project
    ~ $ cd ideal_gas_project/

We then proceed by initializing the data space within a Python script called ``init.py``:

.. code:: python

    # init.py
    import signac

    project = signac.init_project()

    for p in range(1, 10):
        sp = {"p": p, "kT": 1.0, "N": 1000}
        job = project.open_job(sp).init()

The :py:func:`signac.init_project` function initializes the **signac** project in the current working directory by creating a hidden ``.signac`` subdirectory.
The location of this directory defines the *project path*.
Initially, the ``.signac`` directory will contain the minimal configuration information required to define the project.

.. code:: bash

    ~/ideal_gas_project $ python init.py
    ~/ideal_gas_project $ ls -a
    .               ..              .signac         init.py         workspace
    ~/ideal_gas_project $ ls .signac
    config
    ~/ideal_gas_project $ cat .signac/config
    schema_version = 2


We can access the project interface from anywhere within the project path or its subdirectories by calling the :py:func:`signac.get_project` function, or from outside this directory by providing an explicit path, *e.g.*, ``signac.get_project('/path/to/ideal_gas_project')``.

We can verify that the initialization worked by examining the *implicit* schema of the project we just created:

.. code:: bash

    ~/ideal_gas_project $ signac schema
    {
     'N': 'int([1000], 1)',
     'kT': 'float([1.0], 1)',
     'p': 'int([1, 2, 3, ..., 8, 9], 9)',
    }


The output of the ``$ signac schema`` command gives us a brief overview of all keys that were used as well as their values (range).

.. note::

    The ``job.init()`` function is `idempotent <https://en.wikipedia.org/wiki/Idempotence>`_, meaning that it is safe to call it multiple times even after a job has already been initialized.
    It is good practice make *all* steps that are part of the data space initialization routine idempotent.


Exploring the data space
------------------------

The core function that **signac** offers is the ability to associate metadata --- for example, a specific set of parameters such as temperature, pressure, and system size --- with a distinct directory on the file system that contains all data related to said metadata.
The :py:meth:`~signac.Project.open_job` method associates the metadata specified as its first argument with a distinct directory, the *job directory*.
These directories are located in the ``workspace`` subdirectory within the project directory and the directory name is the *job id*.

.. code-block:: bash

    ~/ideal_gas_project $ ls -1 workspace/
    03585df0f87fada67bd0f540c102cce7
    22a51374466c4e01ef0e67e65f73c52e
    71855b321a04dd9ee27ce6c9cc0436f4
    # ...

The *job id* is a highly compact, unambiguous representation of the full metadata, *i.e.*, a distinct set of key-value pairs will always map to the same job id.
However, it can also be somewhat cryptic, especially for users who would like to browse the data directly on the file system.
Fortunately, you don't need to worry about this internal representation of the data space while you are actively working with the data.
Instead, you can create a *linked view* with the ``signac view`` command:

.. code-block:: bash

    ~/ideal_gas_project $ signac view
    ~/ideal_gas_project $ ls -d view/p/*
    view/p/1  view/p/2  view/p/3  view/p/4  view/p/5  view/p/6  view/p/7  view/p/8  view/p/9

Views are designed to provide a human-readable representation of the metadata in the form of a nested directory structure.
The directory hierarchy is composed of a sequence of nested ``key/value`` subdirectories such that the entire metadata associated with a job is encoded in the full path to the view directory.
Each leaf node in the directory tree contains a ``job`` directory, which is a symbolic link to the actual workspace directory:

.. code-block:: bash

    ~/ideal_gas_project $ ls view/p/1
    job

To minimize the directory tree depth, the linked view constructed is the most compact representation of the data space, in the sense that any parameters that do not vary across the entire data space are omitted from the directory tree.
In our example, **signac** detected that the values for *kT* and *N* are constant across all jobs and therefore omitted creating nested subdirectories for them.

.. note::

    Make sure to update the view paths by executing the ``$ signac view`` command (or equivalently with the :py:meth:`~signac.Project.create_linked_view` method) every time you add or remove jobs from your data space.


Interacting with the **signac** project
---------------------------------------

You interact with the **signac** project on the command line using the ``signac`` command.
You can also interact with the project within Python *via* the :py:class:`signac.Project` class.
You can obtain an instance of that class within the project path or its subdirectories with:

.. code-block:: pycon

    >>> import signac
    >>> project = signac.get_project()

.. tip::

    You can use the ``$ signac shell`` command to launch a Python interpreter with ``signac`` already imported.
    If this command is executed within a project directory or a job directory, the additional variables like
    ``project`` and ``job`` will be set to :py:func:`~signac.get_project()` and :py:func:`~signac.get_job()` respectively.


We can then iterate through all jobs in the project:

.. code-block:: pycon

    >>> for job in project:
    ...     print(job)
    ...
    03585df0f87fada67bd0f540c102cce7
    22a51374466c4e01ef0e67e65f73c52e
    71855b321a04dd9ee27ce6c9cc0436f4
    # ...

To iterate over a subset of jobs, use the :py:meth:`~signac.Project.find_jobs` method in combination with a query expression:

.. code-block:: pycon

    >>> for job in project.find_jobs({"kT": 1.0, "p.$lt": 3.0}):
    ...     print(job, job.sp.p)
    ...
    742c883cbee8e417bbb236d40aea9543 1
    ee550647e3f707b251eeb094f43d434c 2
    >>>

In this example we selected all jobs, where the value for :math:`kT` is equal to 1.0 -- which would be all of them -- and where the value for :math:`p` is less than 3.0.
The equivalent selection would be achieved on the command line with ``$ signac find kT 1.0 p.\$lt 3.0``.
See the detailed :ref:`query` documentation for more information on how to find and select specific jobs.

.. note::

    The following expressions are all equivalent: ``for job in project:``, ``for job in project.find_jobs():``, and ``for job in project.find_jobs(None):``.

Operating on the data space
---------------------------

Each job represents a data set associated with specific metadata.
The point is to generate data which is a function of that metadata.
Within the framework's language, such a function is called an *operation*.

Coming back to our example, a very simple operation that calculates the volume :math:`V` might look like this:

.. code-block:: python

    def volume(N, kT, p):
        return N * kT / p

Let's store the volume within our data space in a file called ``volume.txt``, by implementing this function in a Python script called ``project.py``:

.. code-block:: python

    # project.py
    import signac


    def compute_volume(job):
        volume = job.sp.N * job.sp.kT / job.sp.p
        with open(job.fn("volume.txt"), "w") as file:
            file.write(str(volume) + "\n")


    project = signac.get_project()
    for job in project:
        compute_volume(job)

Executing this script will calculate and store the volume for each pressure-temperature combination in a file called ``volume.txt`` within each job's workspace.

.. note::

    The ``job.fn('volume.txt')`` expression is a short-cut for ``os.path.join(job.workspace(), 'volume.txt')``.


Workflows
=========

.. attention::

    The rest of the tutorial describes how to use **signac-flow**, which is no longer maintained.
    Switch to `row <https://row.readthedocs.io>`_.

Implementing a simple workflow
------------------------------

In many cases, it is desirable to avoid the repeat execution of data space operations, especially if they are not `idempotent <https://en.wikipedia.org/wiki/Idempotence>`_ or are significantly more expensive than our simple example.
For this, we will incorporate the ``compute_volume()`` function into a workflow using the package ``signac-flow`` and its :class:`~.flow.FlowProject` class.
We slightly modify our ``project.py`` script:

.. code-block:: python

    # project.py
    from flow import FlowProject


    class Project(FlowProject):
        pass


    @Project.operation
    def compute_volume(job):
        volume = job.sp.N * job.sp.kT / job.sp.p
        with open(job.fn("volume.txt"), "w") as file:
            file.write(str(volume) + "\n")


    if __name__ == "__main__":
        Project().main()

The :py:meth:`~.flow.FlowProject.operation` decorator identifies the ``compute_volume`` function as an *operation function* of our project.
Furthermore, it is now directly executable from the command line via an interface provided by the :py:meth:`~flow.FlowProject.main` method.
Note that we created a (trivial) subclass of ``FlowProject`` rather than using ``FlowProject`` directly.
Operations are associated with a class, not an instance, so encapsulating distinct workflows into separate classes is a good organizational best practice.

We can now execute all operations defined within the project with:

.. code-block:: bash

    ~/ideal_gas_project $ python project.py run
    Using environment configuration: StandardEnvironment
    WARNING:flow.project:Operation 'compute_volume' has no postconditions!

We'll come back to discussing :ref:`environments <environments>` later.
The warning indicates that the ``run`` command will continue to execute all defined operations until they are considered completed.
An operation is considered completed when all its *postconditions* are met, and it is up to the user to define those postconditions.
Since we have not defined any postconditions yet, **signac** would continue to execute the same operation indefinitely.

For this example, a good postcondition would be the existence of the ``volume.txt`` file.
To tell the :py:class:`~.flow.FlowProject` class when an operation is *completed*, we can modify the above example by adding a function that defines this condition:

.. code-block:: python

    # project.py
    from flow import FlowProject


    class Project(FlowProject):
        pass


    def volume_computed(job):
        return job.isfile("volume.txt")


    @Project.post(volume_computed)
    @Project.operation
    def compute_volume(job):
        volume = job.sp.N * job.sp.kT / job.sp.p
        with open(job.fn("volume.txt"), "w") as file:
            file.write(str(volume) + "\n")


    if __name__ == "__main__":
        Project().main()


.. tip::

    Simple conditions can be conveniently defined inline as `lambda expressions`_: ``@FlowProject.post(lambda job: job.isfile("volume.txt"))``.

.. _lambda expressions: https://docs.python.org/3/reference/expressions.html#lambda

We can check that we implemented the condition correctly by executing ``$ python project.py run`` again.
This should now return without any message because all operations have already been completed.

.. note::

    To simply execute a specific operation from the command line ignoring all logic, use the ``exec`` command, *e.g.*: ``$ python project.py exec compute_volume``.
    This command (as well as the run command) also accepts jobs as arguments, so you can specify that you only want to run operations for a specific set of jobs.

Extending the workflow
----------------------

So far we learned how to define and implement operations and how to define simple postconditions to control the execution of said operations.
In the next step, we will learn how to integrate multiple operations into a cohesive workflow.

First, let's verify that the volume has actually been computed for all jobs.
For this we transform the ``volume_computed()`` function into a *label function* by decorating it with the :py:meth:`~flow.FlowProject.label` decorator:

.. code-block:: python

    # ...


    @Project.label
    def volume_computed(job):
        return job.isfile("volume.txt")


    # ...

We can then view the project's status with the ``status`` command:

.. code-block:: bash

    ~/ideal_gas_project $ python project.py status
    Using environment configuration: StandardEnvironment
    Fetching status: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:00<00:00, 27941.33it/s]
    Fetching labels: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 9/9 [00:00<00:00, 58344.26it/s]

    Overview: 9 jobs/aggregates, 0 jobs/aggregates with eligible operations.

    label            ratio
    ---------------  --------------------------------------------------------
    volume_computed  |████████████████████████████████████████| 9/9 (100.00%)

    operation/group
    -----------------


    [U]:unknown [R]:registered [I]:inactive [S]:submitted [H]:held [Q]:queued [A]:active [E]:error [GR]:group_registered [GI]:group_inactive [GS]:group_submitted [GH]:group_held [GQ]:group_queued [GA]:group_active [GE]:group_e
    rror

The labels section shows that 9/9 jobs have the volume_computed label, meaning that there is a ``volume.txt`` file in each and every job directory.

Let's assume that instead of storing the volume in a text file, we wanted to store in it in a `JSON`_ file called ``data.json``.
Since we are pretending that computing the volume is an expensive operation, we will implement a second operation that copies the result stored in the ``volume.txt`` file into the ``data.json`` file instead of recomputing it:

.. _JSON: https://en.wikipedia.org/wiki/JSON

.. code-block:: python

    # project.py
    from flow import FlowProject
    import json

    # ...


    @Project.pre(volume_computed)
    @Project.post.isfile("data.json")
    @Project.operation
    def store_volume_in_json_file(job):
        with open(job.fn("volume.txt")) as textfile:
            data = {"volume": float(textfile.read())}
            with open(job.fn("data.json"), "w") as jsonfile:
                json.dump(data, jsonfile)


    # ...

Here we reused the ``volume_computed`` condition function as a **precondition** and took advantage of the ``post.isfile`` function to define the postcondition for this operation function.

.. important::

    An operation function is **eligible** for execution if all preconditions are met, at least one postcondition is not met and the operation is not currently submitted or running.

Next, instead of running this new function for all jobs, let's test it for one job first.

.. code-block:: bash

    ~/ideal_gas_project $ python project.py run -n 1
    Using environment configuration: StandardEnvironment
    WARNING:flow.project:Reached the maximum number of operations that can be executed, but there are still eligible operations.

We can verify the output with:

.. code-block:: bash

    ~/ideal_gas_project $ cat workspace/742c883cbee8e417bbb236d40aea9543/data.json
    {"volume": 1000.0}

Since that seems right, we can then store all other volumes in the respective ``data.json`` files by executing ``$ python project.py run``.

.. tip::

    We could further simplify our workflow definition by replacing the ``pre(volume_computed)`` condition with ``pre.after(compute_volume)``, which is a shortcut to reuse all of ``compute_volume()``'s postconditions as preconditions for the ``store_volume_in_json_file()`` operation.

Grouping Operations
-------------------

If we wanted to submit :code:`compute_volume` and :code:`store_volume_in_json_file` together to run in series, we currently couldn't, even though we know that :code:`store_volume_in_json_file` can run immediately after :code:`compute_volume`.
With the :py:class:`FlowGroup` class, we can group the two operations together and submit any job that is ready to run :code:`compute_volume`.
To do this, we create a group and decorate the operations with it.

.. code-block:: python

    # ...

    volume_group = Project.make_group(name="volume")


    @volume_group
    @Project.post(volume_computed)
    @Project.operation
    def compute_volume(job):
        volume = job.sp.N * job.sp.kT / job.sp.p
        with open(job.fn("volume.txt"), "w") as file:
            file.write(str(volume) + "\n")


    @volume_group
    @Project.pre(volume_computed)
    @Project.post.isfile("data.json")
    @Project.operation
    def store_volume_in_json_file(job):
        with open(job.fn("volume.txt")) as textfile:
            data = {"volume": float(textfile.read())}
            with open(job.fn("data.json"), "w") as jsonfile:
                json.dump(data, jsonfile)
        Project().main()


    # ...


We can now run :code:`python project.py run -o volume` to run both operations.

The job document
----------------

Storing results in JSON files is good practice because JSON is an open, human-readable format, and parsers are readily available in a wide range of languages.
**signac** stores all metadata in JSON files.
In addition, each job supports storing data in a separate JSON file called the :ref:`job document <project-job-document>`.
Let's add another operation to our ``project.py`` script that stores the volume in the job document:

.. code-block:: python

     # ...


     @Project.pre.after(compute_volume)
     @Project.post(lambda job: "volume" in job.document)
     @Project.operation
     def store_volume_in_document(job):
         with open(job.fn("volume.txt")) as textfile:
             job.document.volume = float(textfile.read())

Besides needing fewer lines of code, storing data in the job document has one more distinct advantage: it is directly searchable.
That means that we can find and select jobs through the signac API (or CLI) based on the contents of their documents.

Executing the ``$ python project.py run`` command after adding the above function to the ``project.py`` script will store all volume in the job documents.
We can then inspect all *searchable* data with the ``$ signac find`` command in combination with the ``--show`` option:

.. code-block:: bash

    ~/ideal_gas_project $ signac find --show
    03585df0f87fada67bd0f540c102cce7
    {'N': 1000, 'kT': 1.0, 'p': 3}
    {'volume': 333.3333333333333}
    22a51374466c4e01ef0e67e65f73c52e
    {'N': 1000, 'kT': 1.0, 'p': 5}
    {'volume': 200.0}
    71855b321a04dd9ee27ce6c9cc0436f4
    {'N': 1000, 'kT': 1.0, 'p': 4}
    {'volume': 250.0}
    # ...

When executed with ``--show``, the ``find`` command not only prints the job id, but also the metadata and the document for each job.
In addition to selecting by metadata as shown earlier, we can also find and select jobs by their job document content, *e.g.*:

.. code-block:: bash

    ~/ideal_gas_project $ signac find doc.volume.\$lte 125 --show
    Interpreted filter arguments as '{"doc.volume.$lte": 125}'.
    df1794892c1ec0909e5955079754fb0b
    {'N': 1000, 'kT': 1.0, 'p': 10}
    {'volume': 100.0}
    dbe8094b72da6b3dd7c8f17abdcb7608
    {'N': 1000, 'kT': 1.0, 'p': 9}
    {'volume': 111.11111111111111}
    97ac0114bb2269561556b16aef030d43
    {'N': 1000, 'kT': 1.0, 'p': 8}
    {'volume': 125.0}


Job.data and Job.stores
-----------------------

The job document is useful for storing small sets of numerical values or textual data.
Text files like JSON are generally unsuitable for large numerical data, however, due to issues with floating point precision as well as sheer file size.
To support storing such data with **signac**, the job :py:attr:`~signac.contrib.job.Job.data` attribute provides a dict-like interface to an HDF5 file, a much more suitable format for storing large numerical data such as NumPy arrays.

.. code-block:: python

      with job.data:
          job.data.my_array = numpy.zeros(64, 32)

You can use the ``data``-attribute to store both built-in types, numpy arrays, and pandas dataframes.
The ``job.data`` property is a shortcut for ``job.stores['signac_data']``, you can access many different data stores by providing your own name, e.g., ``job.stores.my_data``.

See :ref:`project-job-data` for an in-depth discussion.

Submit operations to a scheduling system
========================================

In addition to executing operations directly on the command line, **signac** can also submit operations to a scheduler such as SLURM_.
The ``submit`` command will generate and submit a script containing the operations to run along with relevant scheduler directives such as the number of processors to request.
In addition, **signac** will also keep track of submitted operations in addition to workflow progress, which almost completely automates the submission process as well as preventing the accidental repeated submission of operations.

.. _SLURM: https://slurm.schedmd.com/

To use this feature, make sure that you are on a system with any of the supported schedulers and then run the ``$ python project.py submit`` command.

As an example, we could submit the operation ``compute_volume`` to the cluster.

``$ python project.py submit -o compute_volume -n 1 -w 1.5``

This command submits the next available job to the cluster with a walltime of 1.5 hours (only one job because we specified ``-n 1``).
To inspect the submission script before submitting, use the ``--pretend`` option to print the script to the console.
Here is some sample output used on Stampede2, a SLURM-based queuing system:

.. code-block:: bash

    $ python project.py submit -o compute_volume -n 1 -w 1.5 --pretend
    Query scheduler...
    Submitting cluster job 'ideal_gas/ee550647/compute_volu/0000/085edda24ead71794f423e0046744a17':
     - Operation: compute_volume(ee550647e3f707b251eeb094f43d434c)
    #!/bin/bash
    #SBATCH --job-name="ideal_gas/ee550647/compute_volu/0000/085edda24ead71794f423e0046744a17"
    #SBATCH --partition=skx-normal
    #SBATCH -t 01:30:00
    #SBATCH --nodes=1
    #SBATCH --ntasks=1

    set -e
    set -u

    cd /scratch/05583/tg848827/ideal_gas_project

    # compute_volume(ee550647e3f707b251eeb094f43d434c)
    /opt/apps/intel17/python3/3.6.3/bin/python3 project.py exec compute_volume ee550647e3f707b251eeb094f43d434c

We can submit 5 jobs simultaneously by changing ``-n 1`` to ``-n 5``.
After submitting, if we run ``$ python project.py status -d``, a detailed report is produced that tracks the progress of each job.

.. code-block:: bash

    $ python project.py status -d
    Query scheduler...
    Collect job status info: 100%|██████████████████████████████| 10/10 [00:00<00:00, 2500.48it/s]
    # Overview:
    Total # of jobs: 10

    label    ratio
    -------  -------
    [no labels to show]

    # Detailed View:
    job_id                            operation           labels
    --------------------------------  ------------------  --------
    ee550647e3f707b251eeb094f43d434c  compute_volume [Q]
    df1794892c1ec0909e5955079754fb0b  compute_volume [Q]
    71855b321a04dd9ee27ce6c9cc0436f4  compute_volume [Q]
    dbe8094b72da6b3dd7c8f17abdcb7608  compute_volume [Q]
    a2fa2b860d0a1df3f5dbaaa3a7798a59  compute_volume [Q]
    22a51374466c4e01ef0e67e65f73c52e  compute_volume [U]
    97ac0114bb2269561556b16aef030d43  compute_volume [U]
    03585df0f87fada67bd0f540c102cce7  compute_volume [U]
    e5613a5439caeb021ce40a2fc0ebe7ed  compute_volume [U]
    742c883cbee8e417bbb236d40aea9543  compute_volume [U]
    [U]:unknown [R]:registered [Q]:queued [A]:active [I]:inactive [!]:requires_attention

Jobs signified with ``Q`` are queued in the cluster; when calling ``python project.py status -d`` again, if ``signac`` queries the cluster to find those jobs have begun running, their status will be reported ``A``.

See the :ref:`cluster-submission` section for further details on how to use the ``submit`` option and the :ref:`environments` section for details on submitting to your particular cluster.

.. todo::

    * Add section about signac-dashboard.
