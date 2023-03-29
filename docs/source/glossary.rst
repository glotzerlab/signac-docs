Glossary
========

.. glossary::

   parameter
      A variable, like `T` or `version` or `bench_number`. The smallest unit in signac. Specifically, these are the dictionary keys of the state point.

   state point
      A dictionary of parameters and their values that uniquely specifies a :term:`job`.

   job
      blah

   job directory
      The directory, named for the :term:`job id`, containing all data and metadata pertaining to the given job. Upon initialization of a job, the job directory contains the files `signac_statepoint.json` and `signac_job_document.json`.

   project
      blah

   workspace
      The directory that contains all job directories.

   job id
      A unique MD-5 hash of a job's state point that is used to identify a job.
