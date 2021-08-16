.. _hooks:

=====
Hooks
=====

This chapter provides information setting up hooks at the operation and project level.


.. _hooks_introduction:

Introduction
============

One of the goals of the :py:class:`~signac` framework is to make it easy to track the provenance of research data
and to ensure its reproducibility.
Hooks make it possible to track these state changes in a project.
In general, a hook is a function that is called at a certain time.

Hooks execute code adjacent to key steps of an operation,
such as when it begins, finishes, or fails (called *triggers*).
This helps track where data for each run came from, and which operations were applied to them.
For example, operation failures may be tracked in the job document.
Hooks also make it possible to record the git commit ID upon execution of an operation,
allowing users to track which version of code was used to run the operation.

Hooks can be installed at the :ref:`operation level <_operation_hooks>`
or at the :ref:`flow-project level<_project-level_hooks>`.
Project-level hooks are called for every operation in the flow project.

.. _operation_hooks:

Operation Hooks
===============

Hooks may be added to individual operations using decorators.
The :py:class:`~flow.hook` decorator tells :py:class`~signac` to run a
hook (or set of hooks) when an operation reaches any of the following triggers:
* :py:class:`~flow.hook.on_start` will execute when the operation begins execution.
* :py:class:`~flow.hook.on_finish` will execute when the operation exits, with or without error.
* :py:class:`~flow.hook.on_success` will execute when the operation exits without error.
* :py:class:`~flow.hook.on_fail` will execute when the operation exits with error.

The :py:class:`~flow.hook` decorator accepts objects as a function of the job operation
(:py:class:`~flow.project.JobOperation`).
The decorators :py:class:`~flow.hook.on_start`, :py:class:`~flow.hook.on_start`, and :py:class:`~flow.hook.on_start`
accept functions with two parameters: the operation name and the :py:class:`Job` object.
The decorator :py:class:`hook.on_fail`, accepts functions with three parameters: the operation name, the output error,
and the :py:class:`Job` object.

.. _project-level_hooks:

Project-Level Hooks
===================
placeholder