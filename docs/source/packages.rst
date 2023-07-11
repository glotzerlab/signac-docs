.. _package-overview:

========
Packages
========


The **signac** framework is currently comprised of four packages.
The **synced_collections** package is a standalone package containing data structures used by the core **signac** data management package.
Both **signac-flow** and **signac-dashboard** require the **signac** core package.

The links below lead to the package-specific documentation, including a complete API documentation and changelogs.

.. rubric:: `signac (core) <signac-core_>`_

.. image:: https://img.shields.io/conda/vn/conda-forge/signac
    :target: https://anaconda.org/conda-forge/signac
    :alt: conda-forge signac
.. image:: https://img.shields.io/pypi/v/signac
    :target: https://pypi.org/project/signac/
    :alt: PyPI signac

The *core* **signac** package implements a simple, serverless, distributed database directly on the file system.
It allows users to:

- Manage project data with a well-defined indexable storage layout for data and metadata.
- Search, filter, group, and manipulate the data in existing **signac** projects.
- Create, track, and archive datasets.
- Collaborate on data-intensive projects using a common schema.

.. rubric:: signac-flow_

.. image:: https://img.shields.io/conda/vn/conda-forge/signac-flow
    :target: https://anaconda.org/conda-forge/signac-flow
    :alt: conda-forge signac-flow
.. image:: https://img.shields.io/pypi/v/signac-flow
    :target: https://pypi.org/project/signac-flow/
    :alt: PyPI signac-flow

The **signac-flow** package allows users to:

- Implement reproducible computational workflows for a project data space managed with **signac**.
- Specify operation dependencies with conditions, allowing linear or branched execution
- Run workflows from the command line.
- Submit jobs to high-performance computing (HPC) clusters.

.. rubric:: signac-dashboard_

.. image:: https://img.shields.io/conda/vn/conda-forge/signac-dashboard
    :target: https://anaconda.org/conda-forge/signac-dashboard
    :alt: conda-forge signac-dashboard
.. image:: https://img.shields.io/pypi/v/signac-dashboard
    :target: https://pypi.org/project/signac-dashboard/
    :alt: PyPI signac-dashboard

The **signac-dashboard** package allows users to:

- Browse **signac**-managed data spaces
- Visualize and analyze job data such as text, images, or video.
- Share and collaborate on workspace data through a browser-based GUI.

.. rubric:: synced-collections_

The **synced_collections** package defines data structures that allow users to:

- Transparently synchronize Python objects like lists and dicts with an underlying data store
- Seamlessly translate data from an in-memory Python representation to various storage backends with arbitrary data validation
- Tune for performance using different buffering strategies

These collections are leveraged by **signac** to store and work with data and metadata.

.. _signac-core: https://docs.signac.io/projects/core/
.. _signac-flow: https://docs.signac.io/projects/flow/
.. _signac-dashboard: https://docs.signac.io/projects/dashboard/
.. _synced-collections: https://docs.signac.io/projects/synced_collections/
