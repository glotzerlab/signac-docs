.. _flow-group:

==========
FlowGroups
==========

This chapter provides the information to effectively use multiple operation
groups in submitting and running operations in multiple environments.

.. _flow_group_definition:

Definition
==========

A :py:class:`FlowGroup` is a collection of one or more operation(s) with the
directives associated with that operation. Operations can be in multiple groups
and the directives for an operation can be different in every group that it is
in. Practically, a :py:class:`FlowGroup` acts like a "meta-operation" that can
be submitted and run identical to operations. In factt, within the source code,
all operations are wrapped by singleton groups that handle command generation
and resource requests for that operation.

.. _flow_group_basic_usage:

Basic Usage
===========

While a :py:class:`FlowGroup` is automatically created for each operation, users must
manually create multiple operation groups. Below is an example which creates a
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

To execute or submit ``ex`` alone, use the ``-o`` option to select the group like you would for a
regular operation. Groups are eligible if at least one of their operations
is eligible. Resources are requested appropriately whether groups are run in
serial or parallel.

.. tip::

    To avoid large resource requests, avoid running multiple operation groups in
    parallel. Also, when submitting multiple operation groups in serial, remember
    that the resources requested will match the most computationally intensive
    operation in that group. To avoid wasting compute time, make sure that you group operations
    with similar resource requests or that cheaper operations do not run for long.

.. _flow-group-specify-directives:

Group Specific Directives
=========================

One of the features of :py:class:`FlowGroup` is the ability to assign directives
other than the default to an operation in a given group context. This means that
groups can function as context-specific execution protocols for operations. To
configure group-specific operation directives, use the
:code:`@group.with_directives` decorator provided by the result of
:code:`FlowProject.make_group`. Below shows an example where default and
group specific operation directives are used.

.. code-block:: python
   
    #project.py
    from flow import FlowProject, directives

    class Project(FlowProject):
        pass

    ex = Project.make_group(name='ex')

    @ex.with_directives(directives=dict(ngpu=2))
    @directives(ngpu=1)
    @Project.operation
    def op1(job):
        pass

    @ex.with_directives(directives=dict(nranks=2))
    @directives(nranks=1)
    @Project.operation
    def op2(job):
        pass

    if __name__ == '__main__':
        Project().main()

In this example :code:`op1` requests one GPU if run by itself; however, when run
through the group (i.e. :code:`python project.py run -o ex`), :code:`op1` will
request 2 GPUs. A similar change in MPI ranks requested in :code:`op2` occurs
depending on execution within the group.
