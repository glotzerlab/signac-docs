.. _flow-project:

===============
The FlowProject
===============

This chapter describes how to setup a complete workflow via the implementation of a :py:class:`~flow.FlowProject`.
It includes two **fundamental concepts** for the implementation of workflows with the **signac-flow** package: :ref:`operations <operations>` and :ref:`conditions <conditions>`.

.. _project-setup:

Setup and Interface
===================

To implement an automated workflow using **signac-flow**, we create a subclass of :py:class:`~flow.FlowProject`, here named ``MyProject``:

.. code-block:: python

    # project.py
    from flow import FlowProject

    class MyProject(FlowProject):
        pass

    if __name__ == '__main__':
        MyProject().main()

.. tip::

    The ``$ flow init`` command will generate a minimal ``project.py`` file like the one above.
    There are multiple different templates available via the ``-t/--template`` option.

Executing this script on the command line will give us access to this project's specific command line interface:

.. code-block:: bash

     ~/my_project $ python project.py
     Using environment configuration: StandardEnvironment
     usage: project.py [-h] [-v] [--show-traceback] [--debug] {status,next,run,submit,exec} ...

.. note::

    You can have **multiple** implementations of :py:class:`~flow.FlowProject` that all operate on the same **signac** data space!
    This may be useful, for example, if you want to implement two very distinct workflows that operate on the same data space.
    Simply put those in different modules, *e.g.*, ``project_a.py`` and ``project_b.py``.

.. _operations:

Operations
==========

It is highly recommended to divide individual modifications of your project's data space into distinct functions.

In this context, an *operation* is defined as a function whose only positional argument is an instance of :py:class:`~signac.contrib.job.Job` (in the special case of :ref:`aggregate operations <aggregation>`, variable positional arguments ``*jobs`` are permitted).

We will demonstrate this concept with a simple example.
Let's initialize a project with a few jobs, by executing the following ``init.py`` script within a ``~/my_project`` directory:

.. code-block:: python

    # init.py

    import signac

    project = signac.init_project('MyProject')
    for i in range(10):
        project.open_job({'a': i}).init()

A very simple *operation*, which creates a file called ``hello.txt`` within a job's workspace directory, could be implemented like this:

.. code-block:: python

    # project.py

    from flow import FlowProject

    class MyProject(FlowProject):
        pass

    @MyProject.operation
    def hello(job):
        print('hello', job)
        with job:
            with open('hello.txt', 'w') as file:
                file.write('world!\n')


    if __name__ == '__main__':
        MyProject().main()


.. _conditions:

Conditions
==========

Here the :py:meth:`~flow.FlowProject.operation` decorator function specifies that the ``hello`` operation function is part of our workflow.
If we run ``python project.py run``, **signac-flow** will execute ``hello`` for all jobs in the project.

However, we only want to execute ``hello`` if ``hello.txt`` does not yet exist in the job's workspace.
To do this, we need to create a condition function named ``greeted`` that tells us if ``hello.txt`` already exists in the job workspace:


.. code-block:: python

    def greeted(job):
        return job.isfile('hello.txt')

To complete this component of the workflow, we use the :py:meth:`~flow.FlowProject.post` decorator function to specify that the ``hello`` operation function should only be executed if the ``greeted`` condition is *not* met.

The entirety of the code is as follows:

.. code-block:: python

    # project.py
    from flow import FlowProject


    class MyProject(FlowProject):
        pass


    def greeted(job):
        return job.isfile('hello.txt')


    @MyProject.operation
    @MyProject.post(greeted)
    def hello(job):
        with job:
            with open('hello.txt', 'w') as file:
                file.write('world!\n')


    if __name__ == '__main__':
        MyProject().main()

We can define both :py:meth:`~flow.FlowProject.pre` and :py:meth:`~flow.FlowProject.post` conditions, which allow us to define arbitrary workflows as a `directed acyclic graph <https://en.wikipedia.org/wiki/Directed_acyclic_graph>`__.
A operation is only executed if **all** pre-conditions are met, and at *at least one* post-condition is not met.

.. tip::

    **Cheap conditions should be placed before expensive conditions** as they are evaluated `lazily`_!
    That means for example, that given two pre-conditions, the following order of definition would be preferable:

    .. code-block:: python

        @MyProject.operation
        @MyProject.pre(cheap_condition)
        @MyProject.pre(expensive_condition)
        def hello(job):
            pass

    The same holds for *post*-conditions.

.. _lazily: https://en.wikipedia.org/wiki/Lazy_evaluation

We can then execute this workflow with:

.. code-block:: bash

    ~/my_project $ python project.py run
    Execute operation 'hello(15e548a2d943845b33030e68801bd125)'...
    hello 15e548a2d943845b33030e68801bd125
    Execute operation 'hello(288f97857257baee75d9d84bf0e9dfa8)'...
    hello 288f97857257baee75d9d84bf0e9dfa8
    Execute operation 'hello(2b985fa90138327bef586f9ad87fc310)'...
    hello 2b985fa90138327bef586f9ad87fc310
    # ...

If we implemented and integrated the operation and condition functions correctly, calling the ``run`` command twice should not execute any operations the second time, since the ``greeted`` condition is met for all jobs and the ``hello`` operation should therefore not be executed.

.. tip::

    The ``@with_job`` decorator can be used so the entire operation takes place in the ``job`` context.
    For example:

    .. code-block:: python

        from flow import with_job

        @MyProject.operation
        @MyProject.post(greeted)
        @with_job
        def hello(job):
            with open('hello.txt', 'w') as file:
                file.write('world!\n')

    Is the same as:

    .. code-block:: python

        @MyProject.operation
        @MyProject.post(greeted)
        def hello(job):
            with job:
                with open('hello.txt', 'w') as file:
                    file.write('world!\n')

    This saves a level of indentation and makes it clear the entire operation should take place in the ``job`` context.
    ``@with_job`` also works with the ``@cmd`` decorator but **must** be used first, e.g.:

    .. code-block:: python

        @MyProject.operation
        @with_job
        @cmd
        def hello(job):
            return "echo 'hello {}'".format(job)

The Project Status
==================

The :py:class:`~flow.FlowProject` class allows us to generate a **status** view of our project.
The status view provides information about which conditions are met and what operations are pending execution.

A *label-function* is a condition function which will be shown in the **status** view.
We can convert any condition function into a label function by adding the :py:meth:`~.flow.FlowProject.label` decorator:

.. code-block:: python

    @MyProject.label
    def greeted(job):
        return job.isfile('hello.txt')

We will reset the workflow for only a few jobs to get a more interesting *status* view:

.. code-block:: bash

    ~/my_project $ signac find a.\$lt 5 | xargs -I{} rm workspace/{}/hello.txt

We then generate a *detailed* status view with:

.. code-block:: bash

    ~/my_project $ python project.py status --detailed --stack --pretty
    Collect job status info: 100%|█████████████████████████████████████████████| 10/10
    # Overview:
    Total # of jobs: 10

    label    ratio
    -------  -------------------------------------------------
    greeted  |####################--------------------| 50.00%

    # Detailed View:
    job_id                            labels
    --------------------------------  --------
    0d32543f785d3459f27b8746f2053824  greeted
    14fb5d016557165019abaac200785048
    └● hello [U]
    2af7905ebe91ada597a8d4bb91a1c0fc
    └● hello [U]
    2e6ba580a9975cf0c01cb3c3f373a412  greeted
    42b7b4f2921788ea14dac5566e6f06d0
    └● hello [U]
    751c7156cca734e22d1c70e5d3c5a27f  greeted
    81ee11f5f9eb97a84b6fc934d4335d3d  greeted
    9bfd29df07674bc4aa960cf661b5acd2
    └● hello [U]
    9f8a8e5ba8c70c774d410a9107e2a32b
    └● hello [U]
    b1d43cd340a6b095b41ad645446b6800  greeted
    Legend: ○:ineligible ●:eligible ▹:active ▸:running □:completed

This view provides information about what labels are met for each job and what operations are eligible for execution.
If we did things right, then only those jobs without the ``greeted`` label should have the ``hello`` operation pending.

As shown before, all *eligible* operations can then be executed with:

.. code-block:: bash

    ~/my_project $ python project.py run

Status is determined sequentially by default, because typically the overhead costs of using threads/processes are large.
However, this can be configured by setting a value for the ``flow.status_parallelization`` configuration key.
Possible values are ``thread``, ``process`` or ``none`` with ``none`` being the default value (turning off parallelization).

We can set the ``flow.status_parallelization`` configuration value by directly editing the configuration file(s) or via the command line:

.. code-block:: bash

    ~/my_project $ signac config set flow.status_parallelization process

Check out the :ref:`next section <cluster-submission>` for a guide on how to submit operations to a cluster environment.
