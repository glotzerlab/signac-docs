.. _overview:

Module Overview
===============

**signac** is designed to assist large-scale multidimensional computational data generation and analysis.
Any computational work that requires you to manage files, execute simple to complex workflows may benefit from an integration wit **signac**.
Typical examples include hyperparameter optimization for machine learning applications and high-throughput screening of material properties with varous simulation methods.
It is assumed that the work can be divided into so called *projects*, where each project is vaguely confined by roughly similar structured data, e.g., a parameter study.

We define the process of generating or manipulating a specific data set a *job*.
Every job operates on a set of well-defined unique parameters, which define the job's context.
This means that all data is uniquely addressable from the associated parameters.

.. image:: images/signac_data_space.png

The signac framework consists of multiple modules, which address a specific application.
Most users will not need all of these modules to address their specific needs.

The signac database
-------------------

The *core* signac module implements a simple, serverless, distributed database directly on the file system.
It allows you manage files on the file system and associated them with JSON-encoded metadata.

This metadata is immediately searchable, which allows you to find and select data for specific data sub spaces.

.. important::

    Don't confuse *signac*, the name of the framework, and ``signac`` the name of the core Python module.
    The name of the core Python module name is simply ``signac``, because *all* other modules depend on it.

Manage workflows with signac-flow
---------------------------------

The simple definition and execution of workflows is implemented in the *signac-flow* module.

The signac dashboard
--------------------

The *signac-dashboard* allows you to browse your data space in a web browser.
