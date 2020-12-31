.. _package-overview:

========
Packages
========


The **signac** framework is currently comprised of three packages.
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
- Specify workflow dependencies through conditions, allowing execution that can be simple and linear or complex and branched.
- Run workflows from the command line.
- Submit jobs to high-performance computing (HPC) clusters.

.. rubric:: signac-dashboard_

.. image:: https://img.shields.io/conda/vn/conda-forge/signac-dashboard
    :target: https://anaconda.org/conda-forge/signac-dashboard
    :alt: conda-forge signac-dashboard
.. image:: https://img.shields.io/pypi/v/signac-dashboard
    :target: https://pypi.org/project/signac-dashboard/
    :alt: PyPI signac-dashboard

The **signac-dashboard** package allows users to browse **signac**-managed data spaces:

- Visualize and analyze job data such as text, images, or video.
- Share and collaborate on workspace data through a browser-based GUI.

.. _signac-core: https://docs.signac.io/projects/core/
.. _signac-flow: https://docs.signac.io/projects/flow/
.. _signac-dashboard: https://docs.signac.io/projects/dashboard/
