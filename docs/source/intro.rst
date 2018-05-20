.. _introduction:

============
Introduction
============

.. _overview:

Overview
========

The **signac** framework is designed to assist large-scale multidimensional computational data generation and analysis.
Any computational work that requires you to manage files and execute simple to complex workflows may benefit from an integration wit **signac**.
Typical examples include hyperparameter optimization for machine learning applications and high-throughput screening of material properties with varous simulation methods.
It is assumed that the work can be divided into so called *projects*, where each project is vaguely confined by roughly similar structured data, e.g., a parameter study.

We define the process of generating or manipulating a specific data set a *job*.
Every job operates on a set of well-defined unique parameters, which define the job's context.
This means that all data is uniquely addressable from the associated parameters.

.. image:: images/signac_data_space.png

.. _package-overview:

Packages
========

The signac framework is split into multiple packages, all of which address the needs of a specific application.
Most users will not need *all* packages.

signac: The core package
------------------------

The *core* ``signac`` package implements a simple, serverless, distributed database directly on the file system.
It allows you manage files on the file system and associated them with JSON-encoded metadata.

This metadata is immediately searchable, which allows you to find and select data for specific data sub spaces.

.. important::

    Don't confuse *signac*, the name of the framework, and ``signac`` the name of the core Python module.
    The name of the core Python module name is simply ``signac``, because *all* other packages depend on it.

signac-flow: Implement and execute workflows
--------------------------------------------

The `signac-flow` package is allows us to implement simple to complex workflows that operate on a *data space* managed with signac.
These workflows can be executed directly on the command line or submitted to a cluster scheduling system, which is relevant for users who work in high-performance computing (HPC) environments.

signac-dashboard: Visualize data spaces in the browser
------------------------------------------------------

The `signac-dashboard` package is the latest addition to the **signac** framework.
It allows users to browser their **signac**-managed data spaces in a web browser.
The dashboard can be used for visualiztaion and analysis and is very helpful when sharing data with collaborators.
