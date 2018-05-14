.. _tips-and-tricks:

Tips and Tricks
===============

This is a collection of miscellaneous tips that might help new users to avoid common mistakes or provide a hint to experienced users that just didn't fit anywhere else.

Do not replicate job metadata in file names.
--------------------------------------------

Many users, especially those new to **signac**, fall into the trap to replicate metadata, which is already captured as part of the job metadata, in filenames that are part of the job's workspace.

Taking the project from the tutorial as an example.
Instead of storing the gas volume in a file called ``volume.txt``, we might have stored the volume for a specific pressure in a file called ``volume_pressure_4.txt``.
That is annoying, because now, if we wanted to extract the volume for a given job, instead of:

.. code-block:: python

    volume = float(open(job.fn('volume.txt')).read())

We need to adjust the filename for each job:

.. code-block:: python

    volume = float(open(job.fn('volume_pressure_{}.txt'.format(job.sp.p))).read())

In general, it is desirable to keep the filenames across the workspace as uniform as possible.

Do not hard-code job ids in your scripts.
-----------------------------------------

While it is perfectly fine to copy & paste job ids during interactive work or for small tests, hard-coded job ids within the code are almost always a bad sign.
One of the main advantageous of using **signac** for data management, is that the schema is flexible and may be migrated at any time without too much hazzle.
That also means that existing ids will change and scripts that used them in a hard-coded fashion will fail.

Whenever you find yourself hard-coding ids into your code, consider to replace it with a function that uses the :py:meth:`~.signac.Project.find_jobs` function instead.


How to design a good schema.
----------------------------

There is really no good answer on how to *generally* design a good schema, it very much depends on the domain and the specific application, but there are some basic rules that one might want to follow:

  1. Be descriptive. Although we are using short variable names in the tutorial, in general metadata keys should be as long as necessary, such that a third party might understand their meaning without needing to ask someone.
  2. Any parameter which is likely to be *varied* at some point during the study should be part of the metadata right from the start to avoid needing to migrate the schema later.
  3. Take advantage of grouping keys! The job metadata mapping may be nested, just like any other Python dict.
  4. Even if you don't use "official" schemas, consider to work out standardized schemas among your peers or with your collaborators.
