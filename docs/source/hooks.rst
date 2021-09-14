.. _hooks:

=====
Hooks
=====

.. _hooks_introduction:

Introduction
============

One of the goals of the :py:class:`~signac` framework is to make it easy to track the provenance of research data
and to ensure its reproducibility.
Hooks make it possible to track these state changes in a project.
In general, a hook is a function that is called at a specific point relative to the execution of an operation.

Hooks execute code adjacent to key steps of an operation,
such as when it begins, finishes, or fails. These events are
called triggers with respect to hooks.
Hooks help track where the data for each execution came from, and which operations were applied to them.
For example, operation failures may be tracked in the job document.
Hooks also make it possible to record the git commit ID upon execution of an operation,
allowing users to track which version of code was used to run the operation.

Hooks can be installed at the :ref:`operation level <operation hooks>`
or at the :ref:`flow-project level<project-level hooks>`.
Project-level hooks are called for every operation in the flow project.

.. note::

    Hooks are run in the environment of the python process from which you call **flow**.
    For this reason,
    hooks will not have access to modules in a container if you use that as your execution directive.

.. _operation hooks:

Operation Hooks
===============

Hooks may be added to individual operations using decorators.
The :py:class:`~flow.add_hook` decorator tells :py:class`~signac` to run a
hook (or set of hooks) when an operation reaches any of the following triggers:
* :py:meth:`~flow.add_hook.on_start` will execute when the operation begins execution.
* :py:meth:`~flow.add_hook.on_finish` will execute when the operation exits, with or without error.
* :py:meth:`~flow.add_hook.on_success` will execute when the operation exits without error.
* :py:meth:`~flow.add_hook.on_fail` will execute when the operation exits with error.

The :py:class:`~flow.add_hook` decorator accepts objects as a function of the job operation
(:py:class:`~flow.project.JobOperation`).
The decorators :py:meth:`~flow.add_hook.on_start`, :py:meth:`~flow.add_hook.on_finish`, and :py:class:`~flow.add_hook.on_start`
accept functions with two parameters: the operation name and the :py:class:`Job` object.
The decorator :py:meth:`~flow.add_hook.on_fail`, accepts functions with three parameters: the operation name, the output error,
and the :py:class:`Job` object.

:py:class:`~flow.add_hook` can be used to store basic information about the execution of a job operation to the job document.

In the following example, either the function ``store_success_to_doc`` executes after the
:py:class:`~flow.project.JobOperation`, ``foo``, exits without error, or ``store_error_to_doc`` executes after ``foo``
exits with error:

.. code-block:: python

    # project.py
    from flow import FlowProject

    class Project(FlowProject):
        pass

    def store_success_to_doc(operation_name, job):
        job.doc.update({f'{operation_name}_success': True})

    def store_error_to_doc(operation_name, error, job):
        job.doc.update({f'{operation_name}_success': False})

    @FlowProject.operation
    @FlowProject.add_hook.on_success(store_success_to_doc)
    @FlowProject.add_hook.on_fail(store_error_to_doc)
    @FlowProject.post.isfile("result.txt")
    def foo(job):
        if job.sp.a == 0:
            # Have jobs with statepoint 'a' == 0 fail
            raise ValueError

    if __name__ == '__main__':
       FlowProject().main()

If ``foo`` is executed using ``python project.py run -o foo -f a 1``, the hook triggered ``on_success`` will run,
and ``job.doc.get("foo_success") == True``.

If ``foo`` is executed using ``python project.py run -o foo -f a 0``, a ``ValueError`` is raised.
The hook triggered ``on_fail`` will run, and ``job.doc.get("foo_success") == False``.

.. note::

    Unlike :py:meth:`~flow.add_hook.on_start`, :py:meth:`~flow.add_hook.on_finish`, and :py:meth:`~flow.add_hook.on_on_success`,
    which accept functions that take ``operation_name`` and ``job`` as arguments,
    :py:meth:`~flow.add_hook.on_fail` accepts functions that take ``operation_name``, ``error``, and ``job`` as arguments.

.. _project-level hooks:

Project-Level Hooks
===================

In some cases, it may be desirable to install the same hook or set of hooks for all operations in a project.
A custom set of hooks may be installed by a custom ``install_hooks`` method:

.. code-block:: python

    # project.py
    from flow import FlowProject #etc

    class Project(FlowProject):
        pass

    ...  # Define various job operations

    def set_job_doc(key):
        def set_true(operation_name, job):
            job.doc[f"{operation_name}_{key}"] = True
        return set_true

    def set_job_doc_with_error():
        def set_false(operation_name, error, job):
            job.doc[f"{operation_name}_success"] = True
        return set_false

    class ProjectLevelHooks:

        def install_hooks(self, project):
            project.hooks.on_start.append(set_job_doc("start"))
            project.hooks.on_success.append(set_job_doc("success"))
            project.hooks.on_fail.append(set_job_doc_with_error())
            return project


    if __name__ == '__main__':
        ProjectLevelHooks().install_hooks(Project()).main()
