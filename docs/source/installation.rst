.. _installation:

============
Installation
============

.. _conda: https://anaconda.org/
.. _conda-forge: https://conda-forge.github.io
.. _pip: https://docs.python.org/3.5/installing/index.html

All packages that are part of the **signac** framework depend on the core package, simply named ``signac``, which provides the core data management functionality to all other packages.
See the :ref:`package-overview` section for more information.

Most users should install the ``signac`` and the ``signac-flow`` packages, which are tested for Python version 2.7.x and 3.4+ and do not have any *hard* dependencies, that means you don't have to install any additional dependencies for the basic functionality.
Please see the individual package documentation for instructions on how to install additional packages.

Install with conda
==================

The recommended installation method for installing **signac** packages is *via* conda_.
The **signac** packages are distributed *via* the conda-forge_ channel.
For a standard installation, execute:

.. code-block:: bash

    $ conda install -c conda-forge signac signac-flow

.. tip::

    Consider to add the conda-forge_ channel to your default channels with: ``$ conda config --add channels conda-forge``.

Install with pip
================

For a standard installation with pip_, execute:

.. code:: bash

    $ pip install signac signac-flow

.. note::

    It is recommended to install Python packages into the user space by adding the ``--user`` option to the install command.

Source Code Installation
========================


Alternatively, you can clone any of the package's source code repositories and install them manually.
For example, to install the signac core package, execute the following code:

.. code:: bash

  git clone https://bitbucket.org/glotzer/signac.git
  cd signac
  python setup.py install

.. note::

    It is recommended to install Python packages into the user space by adding the ``--user`` option to the install command.
