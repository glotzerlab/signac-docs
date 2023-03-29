.. _introduction:
.. _overview:

=======
Concept
=======

The **signac** framework is designed to simplify the storage, generation and analysis of multidimensional data sets associated with large-scale, file-based computational studies.
Any computational work that requires you to manage files and execute workflows may benefit from an integration with **signac**.
Typical examples include hyperparameter optimization for machine learning applications and high-throughput screening of material properties with various simulation methods.

In **signac**, collections of parameter values are *jobs* and are stored in a flat directory structure.
Every job is defined by a unique set of well-defined parameters that define the job's context, and it also contains all the data associated with this metadata.
This means that all data is uniquely addressable from the associated parameters.
With **signac**, we define the processes generating and manipulating a specific data set as a sequence of operations on a job.
Using this abstraction, **signac** can define workflows on an arbitrary **signac** workspace.

.. image:: images/signac_data_space.png
