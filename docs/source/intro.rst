.. _introduction:

============
Introduction
============

.. _overview:


Overview
========

The **signac** framework is designed to simplify the storage, generation and analysis of multidimensional data sets associated with large-scale, file-based computational studies.
Any computational work that requires you to manage files and execute workflows may benefit from an integration with **signac**.
Typical examples include hyperparameter optimization for machine learning applications and high-throughput screening of material properties with various simulation methods.
The data model assumes that the work can be divided into so called *projects*, where each project is roughly confined by similarly structured data, e.g., a parameter study.

In **signac**, the elements of a project's data space are called *jobs*.
Every job is defined by a unique set of well-defined parameters that define the job's context, and it also contains all the data associated with this metadata.
This means that all data is uniquely addressable from the associated parameters.
With **signac**, we define the processes generating and manipulating a specific data set as a sequence of operations on a job.
Using this abstraction, **signac** can define workflows on an arbitrary **signac** data space.

.. image:: images/signac_data_space.png

.. _package-overview:


Packages
========

The signac framework is split into multiple packages, all of which address specific needs.
Most users will not need *all* packages.
Many of these packages have their own documentation that provides greater detail on their specific modes of operation than this one, which is intended to provide an overview of the framework as a whole.

.. todo::

    Point to documentation of individual packages.

signac: Data management
------------------------

The *core* ``signac`` package implements a simple, serverless, distributed database directly on the file system.
It allows you manage files on the file system and associate them with JSON-encoded metadata.

This metadata is immediately searchable, which allows you to find and select data for specific data sub spaces.

.. important::

    Don't confuse **signac**, the name of the framework, and ``signac`` the name of the core Python module.
    The name of the core Python module name is simply ``signac``, because *all* other packages in the framework
    depend on it.


signac-flow: Implement and execute workflows
--------------------------------------------

The `signac-flow` package allows us to implement workflows that operate on a *data space* managed with signac.
These workflows range from simple, linear workflows, to large workflows with complex dependencies between operations.
These workflows can be executed directly on the command line or submitted to a cluster scheduling system, which is relevant for users who work in high-performance computing (HPC) environments.


signac-dashboard: Visualize data spaces in the browser
------------------------------------------------------

The `signac-dashboard` allows users to browse their **signac**-managed data spaces through a web-based GUI.
The dashboard can be used for visualization and analysis and is very helpful when sharing data with collaborators.
