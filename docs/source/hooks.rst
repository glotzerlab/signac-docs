.. _hooks:

=====
Hooks
=====

.. _hooks_introduction:

Introduction
============

One of the goals of the **signac** framework is to make it easy to track the provenance of research data and to ensure its reproducibility.
Hooks make it possible to execute user-defined functions before or after :ref:`FlowProject <flow-project>` operations act on a **signac** project.
For example, hooks can be used to track state changes before and after each operation.

A hook is a function that is called at a specific time relative to the execution of a **signac-flow** :ref:`operation <operations>`.
A hook can be triggered when an operation starts, exits, succeeds, or raises an exception.

A basic use case is to log the success/failure of an operation by creating a hook that sets a job document value ``job.doc.operation_success`` to ``True`` or ``False``.
As another example, a user may record the `git commit ID <https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History>`_ upon the start of an operation, allowing them to track which version of code ran the operation.

.. _hook_triggers:

Triggers
========

The following triggers are provided:

1. :py:meth:`~flow.FlowProject.operation_hooks.on_start` will execute when the operation begins execution.
2. :py:meth:`~flow.FlowProject.operation_hooks.on_exit` will execute when the operation exits, with or without an exception.
3. :py:meth:`~flow.FlowProject.operation_hooks.on_success` will execute when the operation exits without an exception.
4. :py:meth:`~flow.FlowProject.operation_hooks.on_exception` will execute when the operation exits with an exception.

Hooks can be installed at the :ref:`operation level <operation-hooks>` or at the :ref:`FlowProject level <project-level-hooks>`.
FlowProject-level hooks are called for every operation in the FlowProject.

Hooks triggered by :py:meth:`~flow.FlowProject.operation_hooks.on_start`, :py:meth:`~flow.FlowProject.operation_hooks.on_exit`, and :py:meth:`~flow.FlowProject.operation_hooks.on_success` are called with two arguments: the operation name (or group name) and the :py:class:`signac.contrib.job.Job` object (or ``*jobs`` if used with aggregation).
Hooks triggered by :py:meth:`~flow.FlowProject.operation_hooks.on_exception` are called with three arguments: the operation name (or group name), the exception raised, and the job (or ``*jobs`` if used with aggregation).

.. note::

    Hooks are run in the Python process where ``FlowProject.main()`` is called.
    For this reason, hooks will not have access to modules in a container specified in the :term:`executable directive <executable>`.

.. _operation-hooks:

Operation Hooks
===============

Hooks may be added to individual operations using decorators.
The :py:class:`~flow.FlowProject.operation_hooks` decorator tells **signac-flow** to run a hook (or set of hooks) when an operation reaches the specified trigger.

An operation hook can be used to store basic information about the execution of a job operation in the job document.
In the following example, if the test operation ``error_on_a_0`` raises an exception, the hook function ``store_error_to_doc`` will be executed.
Otherwise, ``store_success_to_doc`` will be executed.

.. code-block:: python

    # project.py
    from flow import FlowProject

    class Project(FlowProject):
        pass

    def store_success_to_doc(operation_name, job):
        job.doc.update({f'{operation_name}_success': True})

    def store_error_to_doc(operation_name, error, job):
        job.doc.update({f'{operation_name}_success': False})

    @Project.operation
    @Project.operation_hooks.on_success(store_success_to_doc)
    @Project.operation_hooks.on_exception(store_error_to_doc)
    def error_on_a_0(job):
        if job.sp.a == 0:
            raise RuntimeError("Cannot process jobs with a == 0.")

    if __name__ == '__main__':
        Project().main()


If the operation ``error_on_a_0`` is executed on jobs with state point key ``a`` equal to 1 using ``python project.py run --operation error_on_a_0 --filter a 1``, the ``on_success`` hook trigger will run, and ``job.doc.error_on_a_0_success`` will be ``True``.

If the operation ``error_on_a_0`` is executed on jobs with state point key ``a`` equal to 0 using ``python project.py run --operation error_on_a_0 --filter a 0``, a ``RuntimeError`` is raised.
The ``on_exception`` hook trigger will run, and ``job.doc.error_on_a_0_success`` will be ``False``.


.. _project-level-hooks:

Project-Level Hooks
===================

It may be desirable to install the same hook or set of hooks for all operations in a project.
In the following example FlowProject, the hook ``track_start_time`` is triggered when each operation starts.
The hook appends the current time to a list in the job document that is named based on the name of the operation.

 .. code-block:: python

    from flow import FlowProject

    class Project(FlowProject):
        pass

    @Project.operation
    @Project.post.true('test_ran')
    def do_operation(job):
        job.doc.test_ran = True

    @Project.operation
    @Project.pre.after(do_operation)
    @Project.post.false('test_ran')
    def undo_operation(job):
        job.doc.test_ran = False

    def track_start_time(operation_name, job):
        import time
        current_time = time.strftime('%b %d, %Y at %l:%M:%S %p %Z')
        doc_key = f'{operation_name}_start_times'
        job.doc.setdefault(doc_key, [])
        job.doc[doc_key].append(current_time)

    if __name__ == '__main__':
        project = Project()
        project.project_hooks.on_start = [track_start_time]
        project.main()


A custom set of hooks may also be installed at the project level by a custom ``install_hooks`` method.

.. code-block:: python

    # project.py
    from flow import FlowProject

    class Project(FlowProject):
        pass

    @Project.operation
    @Project.post.true('test_ran')
    def do_operation(job):
        job.doc.test_ran = True

    # Define custom hooks class.
    class ProjectHooks:

        def set_job_doc(self, key):
            def set_true(operation_name, job):
                job.doc[f"{operation_name}_{key}"] = True
            return set_true

        def set_job_doc_with_error(self, key):
            def set_false(operation_name, error, job):
                job.doc[f"{operation_name}_{key}"] = False
            return set_false

        def install_hooks(self, project):
            project.project_hooks.on_start.append(self.set_job_doc("start"))
            project.project_hooks.on_success.append(self.set_job_doc("success"))
            project.project_hooks.on_exception.append(self.set_job_doc_with_error("success"))
            return project


    if __name__ == '__main__':
        project = Project()
        project = ProjectHooks().install_hooks(project)
        project.main()
