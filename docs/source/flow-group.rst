.. _flow-group:

==========
FlowGroups
==========

This chapter provides information about submitting and running groups of
multiple operations with varying directives.

.. _flow_group_definition:

Definition
==========

A :py:class:`FlowGroup` is a collection of one or more operation(s) with the
directives associated with that operation. An operation can be in multiple groups,
and the directives for an operation can be different in every group that it is
in. Practically, a :py:class:`FlowGroup` acts like a "meta-operation" that can
be submitted and run like an operation. In fact, within the source code,
each operation is wrapped by a singleton group that handles command generation
and resource requests for that operation.

.. _flow_group_basic_usage:

Basic Usage
===========

While a :py:class:`FlowGroup` is automatically created for each operation, users must
manually create multiple operation groups. Below is an example that creates a
group named ``ex`` which contains the operations ``op1`` and ``op2``.

.. code-block:: python

    # project.py
    from flow import FlowProject

    class Project(FlowProject):
        pass

    ex = Project.make_group(name='ex')

    @ex
    @Project.operation
    def op1(job):
        pass

    @ex
    @Project.operation
    def op2(job):
        pass

    if __name__ == '__main__':
        Project().main()

To execute or submit only ``ex``, use the option ``--operation`` (``-o``) to select the group like you would for a
regular operation. A group is eligible if at least one of its operations
is eligible. Resources are requested appropriately whether groups are run in
series or in parallel.

.. tip::

    To avoid large resource requests, avoid running multiple operation groups in
    parallel. Also, when submitting multiple operation groups in serial, note
    that the resources requested will match the most computationally intensive
    operation in that group. To avoid wasting compute time, make sure that you group operations
    with similar resource requests or that cheaper operations do not run for long.

.. _flow-group-specify-directives:

Group-Specific Directives
=========================

One of the features of :py:class:`FlowGroup` is the ability to assign custom directives
to an operation that activate in a given group context. This means that
groups can function as context-specific execution protocols for operations. To
configure group-specific operation directives, use the
:code:`@group.with_directives` decorator provided by the result of
:code:`FlowProject.make_group`. In the following example, :code:`op1` requests one GPU if run by itself or two GPUs if run through the group :code:`ex` (with :code:`python project.py run -o ex`).

.. code-block:: python
   
    # project.py
    from flow import FlowProject, directives

    class Project(FlowProject):
        pass

    ex = Project.make_group(name='ex')

    @ex.with_directives(directives=dict(ngpu=2))
    @directives(ngpu=1)
    @Project.operation
    def op1(job):
        pass


    if __name__ == '__main__':
        Project().main()
