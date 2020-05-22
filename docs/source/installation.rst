.. _installation:

============
Installation
============

.. _conda: https://anaconda.org/
.. _conda-forge: https://conda-forge.github.io
.. _pip: https://docs.python.org/3/installing/index.html

All packages in the **signac** framework depend on the core **signac** package, which provides the data management functionality used by all other packages (See :ref:`package-overview` for more information).
Most users should install the **signac** and the **signac-flow** packages, which are tested for Python 3.5+ and are built for all major platforms.
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


Build Status
============

signac
------

.. image:: https://img.shields.io/conda/vn/conda-forge/signac
    :target: https://anaconda.org/conda-forge/signac
    :alt: conda-forge signac
.. image:: https://img.shields.io/pypi/v/signac
    :target: https://pypi.org/project/signac/
    :alt: PyPI signac

signac-flow
-----------

.. image:: https://img.shields.io/conda/vn/conda-forge/signac-flow
    :target: https://anaconda.org/conda-forge/signac-flow
    :alt: conda-forge signac-flow
.. image:: https://img.shields.io/pypi/v/signac-flow
    :target: https://pypi.org/project/signac-flow/
    :alt: PyPI signac-flow

signac-dashboard
----------------

.. image:: https://img.shields.io/conda/vn/conda-forge/signac-dashboard
    :target: https://anaconda.org/conda-forge/signac-dashboard
    :alt: conda-forge signac-dashboard
.. image:: https://img.shields.io/pypi/v/signac-dashboard
    :target: https://pypi.org/project/signac-dashboard/
    :alt: PyPI signac-dashboard
