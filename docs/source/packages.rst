.. _package-overview:

==============
Packages
==============

.. toctree::
    :hidden:

    signac (core) <https://docs.signac.io/projects/core/>
    signac-flow <https://docs.signac.io/projects/flow/>
    signac-dashboard <https://docs.signac.io/projects/dashboard/>

The **signac** framework is currently comprised of three packages.
You only have to install those that provide the functionality you need, however both **signac-flow** and **signac-dashboard** require the **signac** core package.

The links below lead to the package-specific documentation, including a complete API documentation and changelogs.

.. rubric:: `signac (core) <signac-core_>`_

The *core* **signac** package implements a simple, serverless, distributed database directly on the file system.
It allows you manage files on the file system and associate them with JSON-encoded metadata.

This metadata is immediately searchable, which allows you to find and select data for specific data sub spaces.

.. rubric:: signac-flow_

The **signac-flow** package allows us to implement workflows that operate on a *data space* managed with signac.
These workflows range from simple, linear workflows, to large workflows with complex dependencies between operations.
These workflows can be executed directly on the command line or submitted to a cluster scheduling system, which is relevant for users who work in high-performance computing (HPC) environments.

.. rubric:: signac-dashboard_

The **signac-dashboard** allows users to browse their **signac**-managed data spaces through a web-based GUI.
The dashboard can be used for visualization and analysis and is very helpful when sharing data with collaborators.

.. _signac-core: https://docs.signac.io/projects/core/
.. _signac-flow: https://docs.signac.io/projects/flow/
.. _signac-dashboard: https://docs.signac.io/projects/dashboard/
