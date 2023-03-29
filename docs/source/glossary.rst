Glossary
========

.. glossary::

   parameter
      A variable, like `T` or `version` or `bench_number`. The smallest unit in **signac**. Specifically, these are the dictionary keys of the state point.

   state point
      A dictionary of parameters and their values that uniquely specifies a :term:`job`, kept in sync with the file `signac_statepoint.json`.

   job
      An object holding data and metadata of a :term:`state point`.

   job directory
      The directory, named for the :term:`job id`, created when a job is initialized containing all data and metadata pertaining to the given job.

   job id
      A unique MD-5 hash of a job's state point that is used to identify a job.

   job document
      A persistent dictionary for storage of simple key-value pairs in a job, kept in sync with the file `signac_job_document.json`.
   
   project
      The primary interface to access and work with jobs and their data.

   workspace
      The directory that contains all job directories of a **signac** project.

   project schema
      The emergent database schema as defined by jobs in the project workspace. The set of all keys present in all state points, as well as their range of values.

   signac schema
      a database schema that defines how signac reads configuration options, currently on v2.


   
