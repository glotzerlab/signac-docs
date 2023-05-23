.. _installation:

============
Installation
============

.. _conda: https://anaconda.org/
.. _conda-forge: https://conda-forge.github.io
.. _pip: https://docs.python.org/3/installing/index.html

The **signac** framework consists of four packages: **signac**, **signac-flow**, **signac-dashboard**, and **synced_collections**.
The **synced_collections** package is a standalone package containing data structures used by the core **signac** package.
All other packages in the **signac** framework depend on **signac** core, which provides the data management functionality used by all other packages.
Most users should install **synced_collections** **signac** and the **signac-flow** packages, which are tested for Python 3.8+ and are built for all major platforms.
For more details about the functionalities of individual packages, please see :ref:`package-overview`.


Install with conda
==================

The recommended installation method for installing **signac** packages is *via* conda_.
The **signac** packages are distributed *via* the conda-forge_ channel.
For a standard installation, execute:

.. code-block:: bash

    $ conda install -c conda-forge signac signac-flow

.. note::

    The synced_collections package is not yet available via conda and must be installed either from source or via pip.

.. tip::

    Consider adding the conda-forge_ channel to your default channels with: ``$ conda config --add channels conda-forge``.


Install with pip
================

For a standard installation with pip_, execute:

.. code:: bash

    $ pip install synced_collections signac signac-flow


Installation from Source
========================

Alternatively, you can clone any of the packages' source code repositories and install them manually.
For example, to install the signac core package you can execute the following code:

.. code:: bash

  # Option 1
  git clone https://github.com/glotzerlab/signac.git
  cd signac
  pip install .

  # Option 2
  pip install git+https://github.com/glotzerlab/signac.git


Build Status
============

synced_collections
------------------

.. image:: https://img.shields.io/pypi/v/synced_collections
    :target: https://pypi.org/project/synced_collections/
    :alt: PyPI synced_collections

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
