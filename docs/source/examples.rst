.. _examples:

========
Examples
========

.. sidebar:: License

    All the code shown here can be downloaded from the signac-docs_ repository, and is released into the `public domain <https://github.com/glotzerlab/signac-docs/blob/master/examples/LICENSE.txt>`_.

.. _signac-docs: https://github.com/glotzerlab/signac-docs

This is a collection of example projects which are designed to illustrate how to implement certain applications and solutions with **signac**.
Unlike the tutorial, the examples consist mainly of complete, immediately executable source code with less explanation.

.. _idg_example:

Ideal Gas
=========

This example is based on the :ref:`tutorial` and assumes that we want to model a system using the ideal gas law:

.. math::

    p V = N k_B T

The data space is initialized for a specific system size :math:`N`, thermal energy :math:`kT`, and pressure :math:`p` in a script called ``init.py``:

.. literalinclude:: ../../examples/tutorial/init.py

The workflow consists of a ``compute_volume`` operation that computes the volume based on the given parameters and stores it within a file called ``V.txt`` within each job's workspace directory.
The two additional operations copy the result into a JSON file called ``data.json`` and into the job document under the ``volume`` key respectively.
All operations are defined in ``project.py``:

.. literalinclude:: ../../examples/tutorial/project.py

The complete workflow can be executed on the command line with ``$ python project.py run``.


MD with HOOMD-blue
==================

This example demonstrates how to setup and analyze the simulation of a Lennard-Jones fluid with molecular dynamics (MD) using `HOOMD-blue <https://glotzerlab.engin.umich.edu/hoomd-blue>`_.
The project data space is initialized in a ``src/init.py`` script with explicit random seed:

.. literalinclude:: ../../examples/hoomd-lj/src/init.py

Using this script, one replica set (for a given random seed, e.g., 42) can then be initialized with:

.. code-block:: bash

    $ python src/init.py 42

The simulation and analysis workflow is broken into three operations:

  1. **init**: Initialize the simulation configuration.
  2. **estimate**: Use the ideal gas law to estimate the expected volume.
  3. **sample**: Carry out the simulation with HOOMD-blue.

Those three operations and corresponding condition functions are defined and implemented within a ``src/project.py`` module:

.. literalinclude:: ../../examples/hoomd-lj/src/project.py

There are two additional label functions, which show whether the simulation has finished (**sampled**) and one that shows the rough progress in quarters (**progress**).

Execute the initialization and simulation with:

.. code-block:: bash

  $ python src/project.py run


.. todo::

    Add Pumpkin example.
    Add MD with Gromacs example.


Integration with Sacred
=======================

Integrating a sacred_ experiment with **signac-flow** is very simple.
Assuming the following sacred_ experiment defined in a ``experiment.py`` module:

.. _sacred: https://sacred.readthedocs.io/

.. literalinclude:: ../../examples/sacred/experiment.py


Then we can integrate that experiment on a *per job* basis like this:

.. literalinclude:: ../../examples/sacred/project.py
