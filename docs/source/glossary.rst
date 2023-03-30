Glossary
========

.. glossary::

   parameter
      A variable, like `T` or `version` or `bench_number`. The smallest unit in **signac**. Specifically, these are the dictionary keys of the state point.

   state point
      A dictionary of parameters and their values that uniquely specifies a :term:`job`, kept in sync with the file `signac_statepoint.json`.

   job
      An object holding data and metadata of the :term:`state point` that defines it.

   job id
      The MD-5 hash of a job's state point that is used to distinguish jobs.

   job directory
      The directory, named for the :term:`job id`, created when a job is initialized that will contain all data and metadata pertaining to the given job.

   job document
      A persistent dictionary for storage of simple key-value pairs in a job, kept in sync with the file `signac_job_document.json`.

   workspace
      The directory that contains all job directories of a **signac** project.

   project
      The primary interface to access and work with jobs and their data stored in the workspace.

   project schema
      The emergent database schema as defined by jobs in the project workspace. The set of all keys present in all state points, as well as their range of values.

   signac schema
      A configuration schema that defines accepted options and values, currently on v2.
