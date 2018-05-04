.. _tutorial:

Tutorial
========

This tutorial is designed to step new users through the basic of setting up a **signac** dataspace, defining and executing a simple workflow, and analyzing the data.

Initializing the data space
---------------------------

For this tutorial, we assume that we are operating on a few files that are associated with two keys *foo* and *bar*, where the *foo* key has values from 0 to 9 and the *bar* value is either True or False.

We start by initializing the data space within a Python script called ``init.py``:

.. code:: Python

    # init.py
    import signac

    project = signac.init_project('my-project')

    for foo in range(9):
        for bar in True, False:
            job = project.open_job(dict(foo=foo, bar=bar))
            job.init()

The :py:func:`signac.init_project` function initializes the **signac** project in the current working directory by creating a file called ``signac.rc``.
The location of this file defines the *project root directory*.
We can access the project interface from anywhere within and below the root directory by calling the :py:func:`signac.get_project` function.

Interacting with the data space
-------------------------------

The signac core function is associate the metadata robustly with the exact path of these directories while we are actively working with the data set.
The :py:meth:`signac.Project.open_job` method associates the metadata specified as its first argument with a distinct directory called a *job workspace*.
These directories are located in the ``workspace`` sub-directory within the project directory.

We can view our project's implicit schema with

.. code:: bash

    $ signac schema
    {
       'bar': 'bool([False, True], 2)',
       'foo': 'int([0, 1, 2, ..., 7, 8], 9)',
    }

The ``$ signac schema`` command gives us a brief description of the implicit schema of our data space.

We can select certain jobs either on the command line or in Python by providing a filter expression:

.. code-block:: Python

    >>> import signac
    >>> project = signac.get_project()
    >>> for job in project.find_jobs({"bar": True}):
    ...     print(job, job.sp.foo)
    ...
    0786b10938b833e1464eaad398c9393b 1
    94be6e79f97048139b05eedbba33c7fd 5
    eaa752dae6771e02f0b25f3b9ceeb667 4
    f768ad275aba928827e926f6d87343e1 7
    64b4d62b29c7f690c8c0b60deb7ac7ee 0
    2763183359d3032f02d554ff212576d4 8
    73dba837a0a2a6bae4bddcc795707f2d 6
    a8a755e402a80d8375012f2b63200aaf 3
    8f70d039e247bca3b2b0d1d32fb68e24 2

The equivalent selection on the command line would be achieved with: ``$ signac find bar true``.
See the `query`_ documenation for more information on searching and selection.

.. _query: http://signac.readthedocs.io/en/latest/query.html

The *job id* is a highly compact, non-ambigious representation of the *full metadata* and has a lot of advantages while *actively working* with the data.
However, it can also be somewhat cryptic, especially for users would like to browse the data on the file system.

For this you can created *linked view* using the ``$ signac view`` on the command line or the :py:meth:`~signac.Project.create_linked_view` method within Python.
This will create a nested directory structure within the ``view`` directory, where each leaf points to the actual workspace directory.
We can inspect that structure with the ``find`` command:

.. code-block:: bash

    $ signac view
    $ find view -print
    view
    view/bar_False
    view/bar_False/foo_0
    view/bar_False/foo_0/job
    view/bar_False/foo_1
    view/bar_False/foo_1/job
    view/bar_False/foo_2
    view/bar_False/foo_2/job
    ...
    view/bar_True
    view/bar_True/foo_0
    view/bar_True/foo_0/job
    view/bar_True/foo_1
    view/bar_True/foo_1/job
    ...

Each ``job`` directory links to the actual workspace directory.
If you are interested in a *permanent* representation of your data space with a nested directory structure, please see `signac-export`_.

.. _signac-export: signac-export

Implementing a simple workflow
------------------------------

Each *signac job* represent a data set associated with specific metadata.
The point is to generate data which is a **function** of that metadata.
Within the framework language, such a function is called a *data space operation*.

We could implement a very simple operation within a `project.py` module like this:

.. code-block:: python

    # project.py

    def foo_is_odd(job):
        print(job.sp.foo, 'even' if job.sp.foo % 2 else 'odd')

This function would print the job's *foo* value and whether it is even to screen.
We could execute this operation for the complete data space by adding a few lines to the script:

.. code-block:: python

    # project.py
    # ...

    if __name__ == '__main__':
        import signac
        project = signac.get_project()
        for job in project:
            foo_is_odd(job)

Executing this, we get roughly this output:

.. code-block:: bash

    $ python project.py
    8 odd
    1 even
    5 even
    8 odd
    7 even
    ...

In a more "useful" application we might want to write our "results" into a file:

.. code-block:: python

    # project.py

    def foo_is_even(job):
        with job:
            with open('is_even.txt') as file:
                file.write("yes" if job.sp.foo % 2 else "no")

    # ...

We can automate and refine this kind of workflow by defining a :py:class:`flow.FlowProject` class as part of the `signac-flow`_ package.

.. _signac-flow: https://signac-flow.readthedocs.io/en/latest


For this, we slightly adjust our `project.py` file:

.. code-block:: python

      from flow import FlowProject


      @FlowProject.operation
      def foo_is_odd(job):
          with job:
              with open('is_even.txt', 'w') as file:
                  file.write('yes' if job.sp.foo % 2 else 'no')


      if __name__ == '__main__':
          FlowProject.main()

We can then execute the same workflow with:

.. code-block:: bash

    $ python project.py execute foo_is_odd


Refining the workflow
---------------------

.. todo::

      * Discuss and showcase labels.
      * Show the status output.
      * Mention cluster submission and link to the full reference.


$ signac-dashboard
------------------

.. todo::

     * Viewing and searching
     * Configuring dashboard settings from the web browser
