.. _installation:

============
Installation
============

.. _conda: https://anaconda.org/
.. _conda-forge: https://conda-forge.github.io
.. _pip: https://docs.python.org/3.5/installing/index.html

All packages in the **signac** framework depend on the core **signac** package, which provides the data management functionality used by all other packages (See :ref:`package-overview` for more information).
Most users should install the **signac** and the **signac-flow** packages, which are tested for Python version 2.7.x and 3.4+ and do not have any *hard* dependencies, ensuring that no packages outside the **signac** framework are required for basic functionality.
Please see the individual package documentation for instructions on how to install additional packages.


Install with conda
==================

The recommended installation method for installing **signac** packages is *via* conda_.
The **signac** packages are distributed *via* the conda-forge_ channel.
For a standard installation, execute:

.. code-block:: bash

    $ conda install -c conda-forge signac signac-flow

.. tip::

    Consider adding the conda-forge_ channel to your default channels with: ``$ conda config --add channels conda-forge``.


Install with pip
================

For a standard installation with pip_, execute:

.. code:: bash

    $ pip install --user signac signac-flow

.. note::

    If you want to install packages for all users on a machine, you can remove the ``--user`` option in the install command.


Installation from Source 
========================

Alternatively, you can clone any of the package's source code repositories and install them manually.
For example, to install the signac core package you can execute the following code:

.. code:: bash

  git clone https://github.com/glotzerlab/signac.git
  cd signac
  python setup.py install --user

.. note::

    If you want to install packages for all users on a machine, you can remove the ``--user`` option in the install command.
