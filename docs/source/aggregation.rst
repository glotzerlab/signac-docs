.. _aggregation:

===========
Aggregation
===========

This chapter provides information about passing aggregates of jobs to operation functions.


.. _aggregator_definition:

Definition
==========

An :py:class:`~flow.aggregator` creates generators of aggregates for use in operation functions via `FlowProject.operation`.
Such functions may accept a variable number of positional arguments, ``*jobs``.
The argument ``*jobs`` is unpacked into an *aggregate*, defined as an ordered tuple of jobs.
See also the Python documentation about :ref:`argument unpacking <python:tut-unpacking-arguments>`.

.. code-block:: python

    # project.py
    from flow import FlowProject, aggregator


    class Project(FlowProject):
        pass


    @Project.operation(aggregator=aggregator())
    def op1(*jobs):
        print("Number of jobs in aggregate:", len(jobs))


    @Project.operation
    def op2(job):
        pass


    if __name__ == "__main__":
        Project().main()

If :py:class:`~flow.aggregator` is used with the default arguments, it will create a single aggregate containing all the jobs present in the project.
In the example above, ``op1`` is an *aggregate operation* where all the jobs present in the project are passed as a variable number of positional arguments (via ``*jobs``), while ``op2`` is an operation where only a single job is passed as an argument.

.. tip::

    The concept of aggregation may be easier to understand if one realizes that "normal" operation functions are equivalent to aggregate operation functions with an aggregate group size of one job.


.. note::

    For an aggregate operation, all conditions like :py:meth:`~flow.FlowProject.pre` or :py:meth:`~flow.FlowProject.post`, callable directives, and other features are required to take the same number of jobs as the operation as arguments.

.. _types_of_aggregation:

Types of Aggregation
====================

Currently, **signac-flow** allows users to aggregate jobs in the following ways:

- *All jobs*: All of the project's jobs are passed to the operation function.
- *Group by state point key(s)*: The aggregates are grouped by one or more state point keys.
- *Group by arbitrary key function*: The aggregates are grouped by keys determined by a key-function that expects an instance of :py:class:`~.signac.contrib.job.Job` and return the grouping key.
- Grouping into aggregates of a specific size.
- Using a completely custom aggregator function when even greater flexibility is needed.

Group By
--------

:py:meth:`~flow.aggregator.groupby` allows users to aggregate jobs by grouping them by a state point key, an iterable of state point keys whose values define the groupings, or an arbitrary callable of :py:class:`~signac.contrib.job.Job`.

.. code-block:: python

    @Project.operation(aggregator=aggregator.groupby("temperature"))
    def op3(*jobs):
        pass

In the above example, the jobs will be aggregated based on the state point key ``"temperature"``.
So, all the jobs having the same value of **temperature** in their state point will be aggregated together.

Groups Of
---------

:py:meth:`~flow.aggregator.groupsof` allows users to aggregate jobs by generating aggregates of a given size.

.. code-block:: python

    @Project.operation(aggregator=aggregator.groupsof(2))
    def op4(job1, job2=None):
        pass

In the above example, the jobs will get aggregated in groups of 2 and hence, up to two jobs will be passed as arguments at once.

.. note::

    In case the number of jobs in the project in this example is odd, there will be one aggregate containing only a single job.
    In general, the last aggregate from :py:meth:`~flow.aggregator.groupsof` will contain the remaining jobs if the aggregate size does not evenly divide the number of jobs in the project.
    If a remainder is expected and valid, users should make sure that the operation function can be called with the reduced number of arguments (e.g. by using ``*jobs`` or providing default arguments as shown above).

Sorting jobs for aggregation
----------------------------

Aggregators allow users to sort the jobs before creating aggregates with the ``sort_by`` parameter.
The sorting order can be defined with the ``sort_ascending`` parameter.
By default, when no ``sort_by`` parameter is specified, the order of the jobs will be decided by the iteration order of the **signac** project.

.. code-block:: python

    @Project.operation(
            aggregator=aggregator.groupsof(2, sort_by="temperature", sort_ascending=False))
    def op5(*jobs):
        pass

.. note::

    In the above example, all the jobs will be sorted by the state point parameter ``"temperature"`` in descending order and then be aggregated as groups of 2.

Selecting jobs for aggregation
------------------------------

**signac-flow** allows users to selectively choose which jobs to pass into operation functions.
This can be used to generate aggregates from only the selected jobs, excluding any jobs that do not meet the selection criteria.

.. code-block:: python

    @Project.operation(aggregator=aggregator(select=lambda job: job.sp.temperature > 0))
    def op6(*jobs):
        pass


.. _aggregate_id:

Aggregate ID
============

Similar to the concept of a job id, an aggregate id is a unique hash identifying an aggregate of jobs.
The aggregate id is sensitive to the order of the jobs in the aggregate.


.. note::

    The id of an aggregate containing one job is that job's id.

In order to distinguish between an aggregate id and a job id, the id of aggregates with more than one job will always have a prefix ``agg-``.

Users can generate the aggregate id of an aggregate using :py:func:`flow.get_aggregate_id`.

.. tip::

    Users can also pass an aggregate id to the ``--job-id`` command line flag provided by **signac-flow** in ``run``, ``submit``, and ``exec``.


.. _aggregation_with_flow_groups:

Aggregation with FlowGroups
===========================

In order to associate an aggregator object with a :py:class:`~flow.project.FlowGroup`, **signac-flow** provides a ``group_aggregator`` parameter in :py:meth:`~flow.FlowProject.make_group`.
By default, no aggregation takes place for a :py:class:`FlowGroup`.

.. note::

    All the operations in a :py:class:`~flow.project.FlowGroup` will use the same :py:class:`~flow.aggregator` object provided to the group's ``group_aggregator`` parameter.

.. code-block:: python

    # project.py
    from flow import FlowProject, aggregator


    class Project(FlowProject):
        pass


    group = Project.make_group("agg-group", group_aggregator=aggregator())


    @group
    @Project.operation(aggregator=aggregator())
    def op1(*jobs):
        pass


    @group
    @Project.operation
    def op2(*jobs):
        pass


    if __name__ == "__main__":
        Project().main()

In the above example, when the group ``agg-group`` is executed using ``python project.py run -o agg-group``, all the jobs in the project are passed as positional arguments for both ``op1`` and ``op2``.
If ``op1`` is executed using ``python project.py run -o op1``, all the jobs in the project are passed as positional arguments because a :py:class:`~flow.aggregator` is associated with the operation function ``op1`` (separately from the aggregator used for ``agg-group``).
If ``op2`` is executed using ``python project.py run -o op2``, only a single job is passed as an argument because no :py:class:`~flow.aggregator` is associated with the operation function ``op2``.
