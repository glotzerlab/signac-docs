.. _tips-and-tricks:
.. _faq:

FAQ
===

This is a collection of frequently asked questions (and their answers) that might help new users avoid common mistakes or provide useful hints to more experienced users.

How do I design a good schema?
------------------------------

There is really no good answer on how to *generally* design a good schema because it is heavily dependent on the domain and the specific application.
Nonetheless, there are some basic rules worth following:

  1. Be descriptive. Although we are using short variable names in the tutorial, in general metadata keys should be as long as necessary for a third party to understand their meaning without needing to ask someone.
  2. Any parameter which is likely to be *varied* at some point during the study should be part of the metadata right from the start to avoid needing to modify the schema later.
  3. Take advantage of grouping keys! The job metadata mapping may be nested, just like any other Python dict.
  4. Even if you don't use "official" schemas, consider to work out standardized schemas among your peers or with your collaborators.
  5. Use the *state point* to define the *identity* of each job, use the *document* to store additional metadata.

What is the difference between the job state point and the job document?
------------------------------------------------------------------------

The *state point* defines the *identity* of each job in form of the *job id*.
Conceptually, all data related to a job should be a function of the *state point*.
That means that any metadata that could be changed without invalidating the data, should in principle be placed in the job document.

.. important::

    The *state point* defines the **identity** of each job, the job document **is data**.


How do I avoid replicating metadata in filenames?
-------------------------------------------------

Many users, especially those new to **signac**, fall into the trap of storing metadata in filenames within a job's workspace even though that metadata is already encoded in the job itself.

Using the :ref:`tutorial` project as an example, we might have stored the volume corresponding to the job at pressure 4 in a file called ``volume_pressure_4.txt``.
However, this is completely unnecessary since that information can already be accessed through the job *via* ``job.sp.p``.
Furthermore, creating files this way causes additional complications, such as the need to modify filenames whenever we operate on the data space.
For example, extracting the volume from a particular job originally consisted of doing this:

.. code-block:: python

    volume = float(open(job.fn("volume.txt")).read())

Now, we instead need to adjust the filename for each job:

.. code-block:: python

    volume = float(open(job.fn("volume_pressure_{}.txt".format(job.sp.p))).read())

In general, it is desirable to keep the filenames across the workspace as uniform as possible.


How do I reference data/jobs in scripts?
----------------------------------------

You can reference other jobs in a script using the path to the project root directory in combination with a query-expression.
While it is perfectly fine to copy & paste job ids during interactive work or for small tests, hard-coded job ids within code are almost always a bad sign.
One of the main advantages of using **signac** for data management is that the schema is flexible and may be migrated at any time without too much hassle.
That also means that existing ids will change and scripts that used them in a hard-coded fashion will fail.

Whenever you find yourself hard-coding ids into your code, consider replacing it with a function that uses the :py:meth:`~.signac.Project.find_jobs` function instead.


How do I achieve optimal performance? What are the practical scaling limits for project sizes?
----------------------------------------------------------------------------------------------

Because **signac** uses a filesystem backend, there are some practical limitations for project size.
While there is no hard limit imposed by signac, some heuristics can be helpful.
On a system with a fast SSD, a project can hold about 100,000 jobs before the latency for various operations (searching, filtering, iteration) becomes unwieldy.
Some **signac** projects have scaled up to around 1,000,000 jobs, but the performance can be slower.
This is especially difficult on network file systems found on HPC clusters, because accessing many small files is expensive compared to accessing fewer large files.
If your project needs to explore a large parameter space with many jobs, consider a state point schema that allows you to do more work with fewer jobs, instead of a small amount of work for many jobs, perhaps by reducing one dimension of the parameter space being explored.
After adding or removing jobs, it is recommended to run the CLI command ``$ signac update-cache`` or the Python method ``Project.update_cache()`` to update the persistent (centralized) cache of all state points in the project.
For workflows implemented with **signac-flow**, the choice of pre-conditions and post-conditions can have a dramatic effect on performance.
In particular, conditions that check for file existence, like ``FlowProject.post.isfile``, are typically much faster than conditions that require reading a file's contents.
