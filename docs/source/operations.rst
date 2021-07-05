.. _basics:




A very simple *operation*, which creates a file called ``hello.txt`` within a job's workspace directory could then be implemented like this:

.. code-block:: python

    # operations.py

    def hello(job):
        print('hello', job)
        with job:
            with open('hello.txt', 'w') as file:
                file.write('world!\n')


We could execute this *operation* for the complete data space, for example in the following manner:

.. code-block:: python

   >>> import signac
   >>> from operations import hello
   >>> project = signac.get_project()
   >>> for job in project:
   ...     hello(job)
   ...
   hello 0d32543f785d3459f27b8746f2053824
   hello 14fb5d016557165019abaac200785048
   hello 2af7905ebe91ada597a8d4bb91a1c0fc
   >>>

The *flow.run()*-interface
--------------------------

However, we can do better.
The flow package provides a command line interface for modules that contain *operations*.
We can access this interface by calling the :py:func:`~.run` function:

.. sidebar:: The *run*-interface

      The :py:func:`.run` function parses the module from where it was called and interprets all **top-level unary functions** as operations.

.. code-block:: python

    # operations.py

    def hello(job):
        print('hello', job)
        with job:
            with open('hello.txt', 'w') as f:
                file.write('world!\n')

    if __name__ == '__main__':
        import flow
        flow.run()

Since the ``hello()`` function is a public, top-level function within the module with only one argument, it is interpreted as a dataspace-operation.
That means we can execute it directly from the command line:

.. code-block:: bash

      ~/my_project $ python operations.py hello
      hello 0d32543f785d3459f27b8746f2053824
      hello 14fb5d016557165019abaac200785048
      hello 2af7905ebe91ada597a8d4bb91a1c0fc

This is a brief demonstration on how to implement the ``operations.py`` module:

.. raw:: html

    <div align="center">
      <script type="text/javascript" src="https://asciinema.org/a/5sj5n5xb11iw9j41lv3obi873.js" id="asciicast-5sj5n5xb11iw9j41lv3obi873" async></script>
    </div>

Parallelized Execution
----------------------

The :py:func:`.run` function automatically executes all operations in parallel on as a many processors as there are available.
We can test that by adding a "cost-function" to our example *operation*:

.. code-block:: python

    from time import sleep

    def hello(job):
        sleep(1)
        # ...

Executing this with ``$ python operations.py hello`` we can now see how many operations are executed in parallel:

.. raw::  html

    <div align="center">
      <script type="text/javascript" src="https://asciinema.org/a/2w8kuoj8h7xde7p22w26obc4i.js" id="asciicast-2w8kuoj8h7xde7p22w26obc4i" async></script>
    </div>

.. _conditions:

Conditions
==========

In the context of signac-flow, a workflow is defined by the **ordered** execution of *operations*.
The execution order is determined by specific *conditions*.

That means in order to implement a workflow, we need to determine two things:

  1. What is the **current state** of the data space?
  2. What needs to happen **next**?

We answer the first question by evaluating unary condition functions for each job.
Based on those *conditions*, we can then determine what should happen next.

Following the example from above, we define a ``greeted`` condition that determines whether the ``hello()`` operation was executed, e.g. the ``hello.txt`` file exists:

.. code-block:: python

    def greeted(job):
        return job.isfile('hello.txt')

Executing this workflow in an ad-hoc manner could be accomplished like this:

.. code-block:: python

    for job in project:
        if not greeted(job):
            hello(job)

This approach is fine for simple workflows, but would become very cumbersome for even slightly more complex workflows and is not very flexible.
In the next chapter, we will demonstrate how to integrate operations and conditions into a well-defined workflow using the :py:class:`~.flow.FlowProject` class.
