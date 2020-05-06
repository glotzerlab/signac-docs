.. _flow-project:

===============
The FlowProject
===============

This chapter describes how to setup a complete workflow via the implementation of a :py:class:`~flow.FlowProject`.

.. _project-setup:

Setup and Interface
===================

To implement a more automated workflow, we can subclass a :py:class:`~flow.FlowProject`:

.. code-block:: python

    # project.py
    from flow import FlowProject

    class Project(FlowProject):
        pass

    if __name__ == '__main__':
        Project().main()

.. tip::

    You can generate boiler-plate templates like the one above with the ``$ flow init`` function.
    There are multiple different templates available via the ``-t/--template`` option.

Executing this script on the command line will give us access to this project's specific command line interface:

.. code-block:: bash

     ~/my_project $ python project.py
     usage: project.py [-h] [-d] {status,next,run,script,submit,exec} ...

.. note::

    You can have **multiple** implementations of :py:class:`~flow.FlowProject` that all operate on the same **signac** project!
    This may be useful, for example, if you want to implement two very distinct workflows that operate on the same data space.
    Simply put those in different modules, *e.g.*, ``project_a.py`` and ``project_b.py``.

.. _workflow-definition:

Defining a workflow
===================

We will reproduce the simple workflow introduced in the previous section by first copying both the ``greeted()`` condition function and the ``hello()`` *operation* function into the ``project.py`` module.
We then use the :py:func:`~flow.FlowProject.operation` and the :py:func:`~.flow.FlowProject.post` decorator functions to specify that the ``hello()`` operation function is part of our workflow and that it should only be executed if the ``greeted()`` condition is not met.

.. code-block:: python

    # project.py
    from flow import FlowProject


    class Project(FlowProject):
        pass


    def greeted(job):
        return job.isfile('hello.txt')


    @Project.operation
    @Project.post(greeted)
    def hello(job):
        with job:
            with open('hello.txt', 'w') as file:
                file.write('world!\n')


    if __name__ == '__main__':
        Project().main()

We can define both *pre* and *post* conditions, which allow us to define arbitrary workflows as an acyclic graph.
A operation is only executed if **all** pre-conditions are met, and at *at least one* post-condition is not met.

.. tip::

    **Cheap conditions should be placed before expensive conditions** as they are evaluated `lazily`_!
    That means for example, that given two pre-conditions, the following order of definition would be preferable:

    .. code-block:: python

        @Project.operation
        @Project.pre(cheap_condition)
        @Project.pre(expensive_condition)
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

If we implemented and integrated the operation and condition functions correctly, calling the ``run`` command twice should produce no output the second time, since the ``greeted()`` condition is met for all jobs and the ``hello()`` operation should therefore not be executed.

.. tip::
   
    The ``@with_job`` decorator can be used so the entire operation takes place in the ``job`` context.
    For example:

    .. code-block:: python

        @Project.operation
        @Project.post(greeted)
        @Project.with_job
        def hello(job):
            with open('hello.txt', 'w') as file:
                file.write('world!\n')

    Is the same as:

    .. code-block:: python

        @Project.operation
        @Project.post(greeted)
        def hello(job):
            with job:
                with open('hello.txt', 'w') as file:
                    file.write('world!\n')
    
    This saves a level of indentation and makes it clear the entire operation should take place in the ``job`` context.
    ``@with_job`` also works with the ``@cmd`` decorator but **must** be used first, e.g.:

    .. code-block:: python

        @Project.operation
        @with_job
        @cmd
        def hello(job):
            return "echo 'hello {}'".format(job)

The Project Status
==================

The :py:class:`~flow.FlowProject` class allows us to generate a **status** view of our project.
The status view provides information about which conditions are met and what operations are pending execution.

A condition function which is supposed to be shown in the **status** view is called a *label-function*.
We can convert any condition function into a label function by adding the :py:meth:`~.flow.FlowProject.label` decorator:

.. code-block:: python

    # project.py
    # ...

    @Project.label
    def greeted(job):
        return job.isfile('hello.txt')

    # ...

We will reset the workflow for only a few jobs to get a more interesting *status* view:

.. code-block:: bash

    ~/my_project $ signac find a.\$lt 5 | xargs -I{} rm workspace/{}/hello.txt

We then generate a *detailed* status view with:

.. code-block:: bash

    ~/my_project.py status --detailed --stack --pretty
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

The status determination is by default parallelized with threads, however this can be turned off or switched to using processes by setting a value for the ``flow.status_parallelization`` configuration key. 
Possible values are ``thread``, ``process`` or ``none`` with the first one being the implicit default value and the last one turning off all parallelization.

We can set the ``flow.status_parallelization`` configuration value by directly editing the configuration file(s) or via the command line, for example:

.. code-block:: bash

    ~/my_project $ signac config set flow.status_parallelization process

.. _project-script:

Generating Execution Scripts
============================

Instead of executing operations directly we can also create a script for execution.
If we have any pending operations, a script might look like this:

.. code-block:: bash

    ~/my_project $ python project.py script

    set -e
    set -u

    cd /Users/csadorf/my_project

    # Operation 'hello' for job '14fb5d016557165019abaac200785048':
    /Users/csadorf/miniconda3/bin/python project.py exec hello 14fb5d016557165019abaac200785048
    # Operation 'hello' for job '2af7905ebe91ada597a8d4bb91a1c0fc':
    /Users/csadorf/miniconda3/bin/python project.py exec hello 2af7905ebe91ada597a8d4bb91a1c0fc
    # Operation 'hello' for job '42b7b4f2921788ea14dac5566e6f06d0':
    /Users/csadorf/miniconda3/bin/python project.py exec hello 42b7b4f2921788ea14dac5566e6f06d0
    # Operation 'hello' for job '9bfd29df07674bc4aa960cf661b5acd2':
    /Users/csadorf/miniconda3/bin/python project.py exec hello 9bfd29df07674bc4aa960cf661b5acd2
    # Operation 'hello' for job '9f8a8e5ba8c70c774d410a9107e2a32b':
    /Users/csadorf/miniconda3/bin/python project.py exec hello 9f8a8e5ba8c70c774d410a9107e2a32b

These scripts can be used for the execution of operations directly, or they could be submitted to a cluster environment for remote execution.
For more information about how to submit operations for execution to a cluster environment, see the :ref:`cluster-submission` chapter.

This script is generated from a default jinja2_ template, which is shipped with the package.
We can extend this default template or write our own to cutomize the script generation process.

.. _jinja2: http://jinja.pocoo.org/

Here is an example for such a template, that would essentially generate the same output:

.. code-block:: bash

    cd {{ project.config.project_dir }}

    {% for operation in operations %}
    operation.cmd
    {% endfor %}

.. note::

    Unlike the default template, this exemplary template would not allow for ``parallel`` execution.

Checkout the :ref:`next section <cluster-submission>` for a guide on how to submit operations to a cluster environment.
