.. _quickstart:

==========
Quickstart
==========

.. todo:: Consider replacing this with a screencast!

To get started, first :ref:`install <installation>` **signac** and then setup a new project with:

.. code-block:: bash

    ~ $ mkdir my_project
    ~ $ cd my_project/
    ~/my_project $ signac init MyProject
    Initialized project 'MyProject'.

.. important::

    If you need to interface with non-Python code, see :ref:`rec_external`.

Once a project has been created, the next step is to initialize the *data space* with, *e.g.*, a script called ``init.py``.:

.. literalinclude:: ../../examples/quickstart/init.py

The key is using the Python *project* handle as the interface to initialize jobs (data points) in your data space.
You can then implement a simple *data space operation* within a ``project.py`` script:

.. literalinclude:: ../../examples/quickstart/project.py

.. currentmodule:: flow

Note the use of the :py:meth:`FlowProject.operation` decorator to indicate that the ``hello_job`` function should be interpreted as an operation acting on the data space.

Operations can be executed for all of your jobs with:

.. code-block:: bash

    ~/my_project $ python project.py run
    Execute operation 'hello_job(15e548a2d943845b33030e68801bd125)'...
    Hello from job 15e548a2d943845b33030e68801bd125, my foo is '1'.
    Execute operation 'hello_job(2b985fa90138327bef586f9ad87fc310)'...
    Hello from job 2b985fa90138327bef586f9ad87fc310, my foo is '2'.
    Execute operation 'hello_job(7f3e901b4266f28348b38721c099d612)'...
    Hello from job 7f3e901b4266f28348b38721c099d612, my foo is '0'.

See the :ref:`tutorial` for a more detailed introduction to how to use **signac** to manage data and implement workflows.
