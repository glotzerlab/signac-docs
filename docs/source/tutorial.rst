.. _tutorial:

========
Tutorial
========

.. sidebar:: License

    The code shown in this tutorial is part of the :ref:`examples`, can be downloaded from the signac-docs_ repository, and is released into the `public domain <https://bitbucket.org/glotzer/signac-docs/raw/master/examples/LICENSE>`_.

.. _signac-docs: https://bitbucket.org/glotzer/signac-docs/

This tutorial is designed to step new users through the basic of setting up a **signac** dataspace, defining and executing a simple workflow, and analyzing the data.


Basics
======


Initializing the data space
---------------------------

For this tutorial, we assume that we want to study pressure-volume (*p-V*) relationship of a nobel gas.
As a first approximation, we could model the gas as an *ideal gas* according to the *ideal gas law*:

.. math::

    p V = N k_B T

Further, we will assume that the calculation of the volume :math:`V` as a function of system size :math:`N`, the Boltzmann constant :math:`k_B`, and temperature :math:`T` is a stand-in for a more expensive simulation.

To test this relationship, we start by creating an empty directory, which is where will place all of our source and the data for this computational study.

.. code:: bash

    ~ $ mkdir ideal_gas_project
    ~ $ cd ideal_gas_project/
    ~/ideal_gas_project $

We then proceed by initializing the data space within a Python script called ``init.py``:

.. code:: python

    # init.py
    import signac

    project = signac.init_project('ideal-gas-project')

    for p in range(1, 10):
        sp = {'p': p, 'kT': 1.0, 'N': 1000}
        job = project.open_job(sp)
        job.init()

The :py:func:`signac.init_project` function initializes the **signac** project in the current working directory by creating a file called ``signac.rc``.
The location of this file defines the *project root directory*.
We can access the project interface from anywhere within and below the root directory by calling the :py:func:`signac.get_project` function.

.. note::

    The name of the project stored in the configuration file is independent of the directory name it resides in.

We can verify the correct intialization by examining the project's *implicit* schema, which we just created:

.. code:: bash

    ~/ideal_gas_project $ signac schema
    {
     'N': 'int([1000], 1)',
     'kT': 'float([1.0], 1)',
     'p': 'int([1, 2, 3, ..., 9, 10], 10)',
    }


The output of the ``$ signac schema`` command gives us a brief overview of all keys that were used as well as their value (range).

.. note::

    The ``job.init()`` function is `idempotent <https://en.wikipedia.org/wiki/Idempotence>`_, that means it is safe to call it multiple times even after a job has already been initialized.
    It is good practice make *all* steps that are part of the data space initialization routine idempotent.


Exploring the data space
------------------------

The signac core function is to associate the provided metadata, such as a specific temperature, pressure, and system size, with a distinct directory on the file system, which contains all data related to said metadata.
The :py:meth:`~signac.Project.open_job` method associates the metadata specified as its first argument with a distinct directory called a *job workspace*.
These directories are located in the ``workspace`` sub-directory within the project directory and the directory name is the so called *job id*.

.. code-block:: bash

    ~/ideal_gas_project $ ls -1 workspace/
    03585df0f87fada67bd0f540c102cce7
    22a51374466c4e01ef0e67e65f73c52e
    71855b321a04dd9ee27ce6c9cc0436f4
    # ...

The *job id* is a highly compact, non-ambigious representation of the *full metadata*.
However, it can also be somewhat cryptic, especially for users who would like to browse the data directly on the file system.
Fortunately, you don't need to worry about this *internal representation* of the data space while you are actively working with the data.

You can create a *linked view* with the ``signac view`` command:

.. code-block:: bash

    ~/ideal_gas_project $ signac view
    ~/ideal_gas_project $ ls view/
    p_1 p_10  p_2 p_3 p_4 p_5 p_6 p_7 p_8 p_9

Each directory contains a ``job`` directory, which is a symbolic link to the actual workspace directory.
The linked view is **the most compact** representation of the data space in form of a nested directory structure.
*Most compact* means in this case, that **signac** detected that the values for *kT* and *N* are constant across all jobs and are therefore safely omitted.

.. note::

    Make sure to update the view paths by executing the ``$ signac view`` command (or equivalently with the :py:meth:`~signac.Project.create_linked_view` method) everytime you add or remove jobs from your data space.

.. todo::

    Add once ``signac-export`` is implemented:
    If you are interested in a *permanent* representation of your data space with a nested directory structure, please see `signac-export`_.

    .. _signac-export: signac-export


Interacting with the **signac** project
---------------------------------------

You interact with the **signac** project on the command line using the ``signac`` command.
You can also interact with the project within Python *via* the :py:class:`signac.Project` class.
You can obtain an instance of that class within the project root directory and all sub-directories with:

.. code-block:: python

    >>> import signac
    >>> project = signac.get_project()

.. todo::

    Introduce ``$ signac-shell`` once relased.

Iterating through all jobs within the data space is then as easy as:

.. code-block:: python

    >>> for job in project:
    ...     print(job)
    ...
    03585df0f87fada67bd0f540c102cce7
    22a51374466c4e01ef0e67e65f73c52e
    71855b321a04dd9ee27ce6c9cc0436f4
    # ...

We can iterate through a select set of jobs with the :py:meth:`~signac.Project.find_jobs` method in combination with a query expression:

.. code-block:: python

    >>> for job in project.find_jobs({"kT": 1.0, "p.$lt": 3.0}):
    ...     print(job, job.sp.p)
    ...
    742c883cbee8e417bbb236d40aea9543 1
    ee550647e3f707b251eeb094f43d434c 2
    >>>

In this example we selected all jobs, where the value for :math:`kT` is equal to 1.0 -- which would be all of them -- and where the value for :math:`p` is less than 3.0.
The equivalent selection on the command line would be achieved with ``$ signac find kT 1.0 p.\$lt 3.0``.
See the detailed `query`_ documentation for more information on how to find and select specific jobs.

.. note::

    The following expressions are all equivalent: ``for job in project:``, ``for job in project.find_jobs():``, and ``for job in project.find_jobs(None):``.

.. _query: http://signac.readthedocs.io/en/latest/query.html

Operating on the data space
---------------------------

Each *signac job* represent a data set associated with specific metadata.
The point is to generate data which is a **function** of that metadata.
Within the framework language, such a function is called a *data space operation*.

Coming back to our example, we could implement a very simple operation that calculates the volume :math:`V` as a function of our metadata like this:

.. code-block:: python

    def volume(N, kT, p):
        return N * kT / p

Let's store the volume within our data space in a file called ``volume.txt``, by implementing this function in a Python script called ``project.py``:

.. code-block:: python

    # project.py
    import signac


    def compute_volume(job):
        volume = job.sp.N * job.sp.kT / job.sp.p
        with open(job.fn('volume.txt'), 'w') as file:
            file.write(str(volume) + '\n')

    project = signac.get_project()
    for job in project:
        compute_volume(job)

Executing this script will calculate and store the volume for each pressure-temperature combination in a file called ``volume.txt`` within each job's workspace.

.. note::

    The ``job.fn('volume.txt')`` expression is a short-cut for ``os.path.join(job.workspace(), 'volume.txt')``.


Workflows
=========

Implementing a simple workflow
------------------------------

In many cases, it is desirable to avoid the repeat execution of *data space operations*, especially if they are not `idempotent <https://en.wikipedia.org/wiki/Idempotence>`_ or significantly more expensive than our simple example.
For this, we will incorporate the ``compute_volume()`` function into a workflow using the :py:class:`~.flow.FlowProject` class.
We slightly modify our ``project.py`` script:

.. code-block:: python

    # project.py
    from flow import FlowProject


    @FlowProject.operation
    def compute_volume(job):
        volume = job.sp.N * job.sp.kT / job.sp.p
        with open(job.fn('volume.txt'), 'w') as file:
            file.write(str(volume) + '\n')


    if __name__ == '__main__':
        FlowProject().main()

The :py:meth:`~.flow.FlowProject.operation` decorator identifies the ``compute_volume`` function as an *operation function* of our project.
Furthermore, it is now directly executable from the command line via an interface provided by the :py:meth:`~flow.FlowProject.main` method.

We can then execute all operations defined within the project with:

.. code-block:: bash

    ~/ideal_gas_project $ python project.py run
    Execute operation 'compute_volume(03585df0f87fada67bd0f540c102cce7)'...
    Execute operation 'compute_volume(22a51374466c4e01ef0e67e65f73c52e)'...
    Execute operation 'compute_volume(71855b321a04dd9ee27ce6c9cc0436f4)'...
    # ...

However, if you execute this in your own terminal, you might have noticed a bunch of warning messages printed out at the end, that read similar to:

.. code-block:: none

    Operation 'compute_volume(03585df0f87fada67bd0f540c102cce7)' exceeds max. # of allowed passes (1).
    Operation 'compute_volume(22a51374466c4e01ef0e67e65f73c52e)' exceeds max. # of allowed passes (1).
    # and so on

That is because by default, the ``run`` command will continue to execute all defined operations, until they are considered *completed*.
An operation is considered completed, when all post conditions are met.
We did not define any post conditions yet, so theoretically, **signac** would continue to execute the same operation indefinitely.

For this example, a good post condition would be the existance of the ``volume.txt`` file.
We can define a condition that tells the :py:class:`~.flow.FlowProject` class when an operation is *completed* like this:

.. code-block:: python

    # project.py
    from flow import FlowProject


    def volume_computed(job):
        return os.path.isfile("volume.txt")


    @FlowProject.operation
    @FlowProject.post(volume_computed)
    def compute_volume(job):
        volume = job.sp.N * job.sp.kT / job.sp.p
        with open(job.fn('volume.txt'), 'w') as file:
            file.write(str(volume) + '\n')


    if __name__ == '__main__':
        FlowProject().main()

.. tip::

    Especially very simple condition functions can be conveniently defined inline as `lambda expression`_: ``@FlowProject.post(lambda job: job.isfile("volume.txt"))``.

.. _lambda expression: https://docs.python.org/3/reference/expressions.html#lambda

We can check that we implemented the condition correctly, by executing ``$ python project.py run`` again, which should now return without any message, because all operations have already been completed.

.. note::

    To simply, execute a specific operation from the command line ignoring all logic, use the ``exec`` command, *e.g.*: ``$ python project.py exec compute_volume``.

Extending the workflow
----------------------

So far we learned how to define and implement *data space operations* and how to define simple post conditions to control the execution of said operations.
In the next step, we will learn how to integrate multiple operations into cohesive workflow.

First, let's verify that the volume has actually been computed for all jobs.
For this we transform the ``volume_computed()`` function into a *label function* by decorating it with the :py:meth:`~flow.FlowProject.label` decorator:

.. code-block:: python

    # project.py
    from flow import FlowProject


    @FlowProject.label
    def volume_computed(job):
        return job.isfile("volume.txt")

    # ...

We can then view the project's status with the ``status`` command:

.. code-block:: bash

    ~/ideal_gas_project $ python project.py status
    Generate output...

    Status project 'ideal-gas-project':
    Total # of jobs: 10

    label            progress
    ---------------  --------------------------------------------------
    volume_computed  |########################################| 100.00%

That means that there is a ``volume.txt`` file in each and every job workspace directory.

Let's assume that instead of storing the volume in a text file, we wanted to store in it in a `JSON`_ file called ``data.json``.
Since we pretend that computing the volume is an expensive operation, we will implement a second operation that copies its result stored in the ``volume.txt`` file into the ``data.json`` file instead of recomputing it:

.. _JSON: https://en.wikipedia.org/wiki/JSON

.. code-block:: python

    # project.py
    from flow import FlowProject
    import json
    # ...

    @FlowProject.operation
    @FlowProject.pre(volume_computed)
    @FlowProject.post.isfile("data.json")
    def store_volume_in_json_file(job):
        with open(job.fn("volume.txt")) as textfile:
            with open(job.fn("data.json"), "w") as jsonfile:
                data = {"volume": float(textfile.read())}
                jsonfile.write(json.dumps(data) + "\n")

    # ...

Here we reused the ``volume_computed`` condition function as a **pre-condition** and took advantage of the ``post.isfile`` short-cut function to define the post-condition for this operation function.

.. important::

    An operation function is **eligible** for execution if all pre-conditions are met, at least one post-condition is not met and the operation is not currently submitted or running.

Next, instead of running this new function for all jobs, let's test it for one job first.

.. code-block:: bash

    ~/ideal_gas_project $ python project.py run -n 1
    Execute operation 'store_volume_in_json_file(742c883cbee8e417bbb236d40aea9543)'...

We can verify the output with:

.. code-block:: bash

    ~/ideal_gas_project $ cat workspace/742c883cbee8e417bbb236d40aea9543/data.json
    {"volume": 1000.0}

That seems right, we can then store all other volumes in the respective ``data.json`` files by executing ``$ python project run``.

.. tip::

    We could further simplify our workflow definition, by replacing the ``pre(volume_computed)`` condition with ``pre.after(compute_volume)``, which is a short-cut to reuse all of ``compute_volume()``'s post-conditions as pre-conditions for the ``store_volume_in_json_file()`` operation.


The job document
----------------

Storing results in JSON-format -- as shown in the previous section -- is good practice, because the JSON format is an open format, human-readable and parsers are available for a large variety of codes.
Because of this, **signac** stores all metadata in JSON-files and in addition comes with a built-in JSON-storage container for each job: the `job document <http://signac.readthedocs.io/en/latest/projects.html#the-job-document>`_.

Let's add another operation to our ``project.py`` script that stores the volume in the *job document*:

.. code-block:: python

   # project.py
   # ...

   @FlowProject.operation
   @FlowProject.pre.after(compute_volume)
   @FlowProject.post(lambda job: 'volume' in job.document)
   def store_volume_in_document(job):
       with open(job.fn("volume.txt")) as textfile:
               job.document.volume = float(textfile.read())

Besides needing fewer lines of code, storing data in the *job document* has one more distinct advantage: it is directly searchable.
That means that we can find and select jobs based on its content.

Executing the ``$ python project.py run`` command after adding the above funtion to the ``project.py`` script will store all volume in the job documents.
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

The ``find`` command in combination with ``--show`` does not only print the *job id*, but also the metadata and the document for each job.
In addition to selecting by metadata as shown earlier, we can also find and select jobs by their *job document* content, *e.g.*:

.. code-block:: bash

    ~/ideal_gas_project $ signac find --doc-filter volume.\$lte 125 --show
    Interpreted filter arguments as '{"volume.$lte": 125}'.
    df1794892c1ec0909e5955079754fb0b
    {'N': 1000, 'kT': 1.0, 'p': 10}
    {'volume': 100.0}
    dbe8094b72da6b3dd7c8f17abdcb7608
    {'N': 1000, 'kT': 1.0, 'p': 9}
    {'volume': 111.11111111111111}
    97ac0114bb2269561556b16aef030d43
    {'N': 1000, 'kT': 1.0, 'p': 8}
    {'volume': 125.0}


Advanced
========

Generating scripts
------------------

So far, we executed all operations directly on the command line with the ``run`` command.
However we can also generate scripts for execution, which is especially relevant if you intend to submit the workflow to a scheduling system typically encountered high-performance computing (HPC) environments.

Scripts are generated using the `jinja2`_ templating system, but you don't have to worry about that unless you want to change any of the default templates.

.. _jinja2: http://jinja.pocoo.org/

We can generate a script for the execution of the *next eligible operations* with the ``script`` command.

We need to reset our workflow before we can test that:

.. code-block:: bash

    ~/ideal_gas_project $ rm -r workspace/
    ~/ideal_gas_project $ python init.py

Let's start by generating a script for the execution of up to two *eligible* operations:

.. code-block:: bash


    ~/ideal_gas_project $ python project.py script -n 2
    set -e
    set -u

    cd /Users/csadorf/ideal_gas_project

    # Operation 'compute_volume' for job '03585df0f87fada67bd0f540c102cce7':
    python project.py exec compute_volume 03585df0f87fada67bd0f540c102cce7
    # Operation 'compute_volume' for job '22a51374466c4e01ef0e67e65f73c52e':
    python project.py exec compute_volume 22a51374466c4e01ef0e67e65f73c52e

By default, the generated script will change into the  *project root directory* and then execute the command for each next eligible operation for all selected jobs.
To run this script, we could pipe it either into a file and then execute it or directly into a command processor with:

.. code-block:: bash

     ~/ideal_gas_project $ python project.py script > run.sh
     ~/ideal_gas_project $ /bin/bash run.sh

Or pipe it directly into the command processor:

.. code-block:: bash

   ~/ideal_gas_project $ python project.py script | /bin/bash
   ~/ideal_gas_project $

Executing the ``script`` command again, we see that it would now execute both the ``store_volume_in_document`` and the ``store_volume_in_json_file`` operation, since both share the same pre-conditions:

.. code-block:: bash

    ~/ideal_gas_project $ python project.py script -n 2
    set -e
    set -u

    cd /Users/csadorf/ideal_gas_project

    # Operation 'store_volume_in_document' for job '03585df0f87fada67bd0f540c102cce7':
    python project.py exec store_volume_in_document 03585df0f87fada67bd0f540c102cce7
    # Operation 'store_volume_in_json_file' for job '03585df0f87fada67bd0f540c102cce7':
    python project.py exec store_volume_in_json_file 03585df0f87fada67bd0f540c102cce7

If we wanted to customize the script generation, we could either extend the base template or simply replace the default template with our own.
To replace the default template, we can put a template script called ``script.sh`` into a directory called ``templates`` within the project root directory.
A simple template script might look like this:

.. code-block:: bash

    cd {{ project.config.project_dir }}

    {% for operation in operations %}
    {{ operation.cmd }}
    {% endfor %}

Storing the above template within a file called ``templates/script.sh`` will now change the output of the ``script`` command to:

.. code-block:: bash

   ~/ideal_gas_project $ python project.py script -n 2
   cd /Users/csadorf/ideal_gas_project

   python project.py exec store_volume_in_document 03585df0f87fada67bd0f540c102cce7
   python project.py exec store_volume_in_json_file 03585df0f87fada67bd0f540c102cce7

Please see ``$ python project.py script --template-help`` to get more information on how to write and use custom templates.

Submit operations to a scheduling system
----------------------------------------

In addition to executing operations directly on the command line and generating scripts, **signac** also supports you in submitting operations to a scheduling system, such as SLURM_.
This is essentially equivalent to generating a script as described in the previous section, but in addition **signac** will also keep track of the submitted operations, to prevent the accidental repeated submission of operations.

.. _SLURM: https://slurm.schedmd.com/

To use this feature, make sure that you are on a system with any of the supported schedulers and then run the ``$ python project.py submit`` command.

.. todo::

    * Add section about signac-dashboard.
