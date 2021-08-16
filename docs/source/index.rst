.. signac documentation master file, created by
   sphinx-quickstart on Fri Oct 23 17:41:32 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the signac framework documentation!
==============================================

The **signac** framework supports researchers in managing project-related data with a well-defined indexable storage layout for data and metadata.
This streamlines post-processing and analysis and makes data collectively accessible.
The **signac** framework aims to help make computational research projects *Transparent*, *Reproducible*, *Usable by others*, and *Extensible* (TRUE) :cite:`Thompson2020`, a set of principles put forth by the MoSDeF Collaboration :cite:`Cummings2021`.

This is the overall **framework documentation**.
It provides a comprehensive overview on what you can do with packages that are part of the **signac** framework.
If you are new to **signac**, the best place to start is to read the :ref:`introduction` and the :ref:`tutorial`.


.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   intro
   packages
   installation
   quickstart
   tutorial
   examples

.. toctree::
   :maxdepth: 1
   :caption: Package API Reference

   signac (core) API <https://docs.signac.io/projects/core/en/latest/api.html>
   signac-flow API <https://docs.signac.io/projects/flow/en/latest/api.html>
   signac-dashboard API <https://docs.signac.io/projects/dashboard/en/latest/api.html>

.. toctree::
   :maxdepth: 2
   :caption: Topic Guide

   projects
   jobs
   query
   dashboard
   flow-project
   cluster_submission
   environments
   templates
   flow-group
   aggregation
   indexing
   collections
   configuration
   recipes
   tips_and_tricks

.. toctree::
   :maxdepth: 2
   :caption: Reference

   community
   scientific_papers
   GitHub <https://github.com/glotzerlab/signac>
   Twitter <https://twitter.com/signacdata>
   license
   acknowledge
   zreferences

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
