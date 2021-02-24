.. _aggregation:

===========
Aggregation
===========

This chapter provides information about the passing aggregates of jobs to operation functions.


.. _aggregator_definition:

aggregator
==========

An :class:`~flow.aggregator` is used as a decorator for an operation function which acts like an
entry point to define the type of aggregation to perform while submitting or running the operation
function.

.. code-block:: python

    # project.py
    from flow import FlowProject, aggregator

    class Project(FlowProject):
        pass

    @aggregator()
    @Project.operation
    def op1(*jobs):
        pass

    @Project.operation
    def op2(job):
        pass

    if __name__ == '__main__':
        Project().main()

By default, if :class:`~flow.aggregator` is used as a decorator, aggregate of all the jobs present
in the project will be created. In the above example, ``op1`` can be referred to as an *aggregate operation*
where all the jobs present in the project are passed as arbitraty arguments (or ``*args``) and ``op2`` is a *normal operation*
where only a single job is passed as a parameter.


.. _types_of_aggregation:

Types of Aggregation
====================

Currently **signac-flow** allows users to aggregate jobs by:

- Grouping them on state point key, an iterable of state point keys whose values define the
  groupings, or an arbitrary callable of :class:`~signac.contrib.job.Job`.
- Generating aggregates of a given size.
- Using custom aggregator function when greater flexibility is needed.

Group By
---------

:class:`~flow.aggregator.groupby` allows users to aggregate jobs by grouping them on
state point key, an iterable of state point keys whose values define the groupings,
or an arbitrary callable of :class:`~signac.contrib.job.Job`.

.. code-block:: python

    @aggregator.groupby('temperature')
    @Project.operation
    def op3(*jobs):
        pass

In the above example, the jobs will get aggregated based on the state point **temperature**.
So, all the jobs having the same value of **temperature** in their state point will be aggregated together.

Groups Of
---------

:class:`~flow.aggregator.groupsof` allows users to aggregate jobs by generating aggregates of a given size.

.. code-block:: python

    @aggregator.groupsof(2)
    @Project.operation
    def op4(job1, job2):
        pass

In the above example, the jobs will get aggregated in groups of 2 and hence, only two jobs will
be passed as parameters at once.

.. note::

    In case the number of jobs in the project is odd, there will be one aggregate containing only a single
    job and hence users should be careful while defining the parameters for an *aggregate operation*.

Sorting jobs for aggregation
----------------------------

**signac-flow** allows users to define the sorting order of jobs before creating the aggregates with the
help of ``sort_by`` parameter and the sorting order can be defined with the help of ``sort_ascending`` parameter.

.. code-block:: python

    @aggregator.groupsof(2, sort_by='temperature', sort_ascending=False)
    @Project.operation
    def op5(job1, job2):
        pass

.. note::

    In the above example, all the jobs will be sorted by the state point parameter ``temperature`` in descending
    order and then be aggregated as groups of 2.

Selecting jobs for aggregation
------------------------------
**signac-flow** allows users to selectively choose which jobs to pass into operation functions.

.. code-block:: python

    @aggregator(select=lambda job: job.sp.temperature > 0)
    @Project.operation
    def op6(job1, job2):
        pass


.. _aggregate_id:

Aggregate ID
============

Similar to the concept of a job id, an aggregate id is a unique hash identifying an aggregate of jobs.
The aggregate id is sensitive to the order of the jobs in the aggregate

.. note::

    The id of an aggregate containing one job is that job's id.

In order to distinguish between aggregate id and a job id, for an aggregate of more than one job
the aggregate id of that aggregate will always have a prefix ``agg-``.

Users can generate the aggregate id of an aggregate using :meth:`flow.get_aggregate_id`.

.. tip::

    Users can also pass an aggregate id to the ``--job-id`` command-line flag provided by **signac-flow**
    in ``run``, ``submit``, and ``exec``.


.. _aggregation_with_flow_groups:

Aggregation with FlowGroups
===========================

