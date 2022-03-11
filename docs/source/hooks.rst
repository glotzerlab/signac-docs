.. _hooks:

=====
Hooks
=====

.. _hooks_introduction:

Introduction
============

One of the goals of the **signac** framework is to make it easy to track the provenance of research data and to ensure its reproducibility.
Hooks make it possible to track state changes to each job in a **signac** project as the :ref:`FlowProject<flow-project>` operates on it.

A hook is a function that is called at a specific point relative to the execution of a **signac-flow** :ref:`operation<operations>`.
A hook is triggered when an operation starts, exits, succeeds, or fails.

A basic use case is to log the success/failure of an operation by creating a hook that sets a job document value ``job.doc.operation_success`` to ``True`` or ``False``.
Additionally, a user may record the `git commit ID <https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History>`_ upon the start of an operation, allowing them to track which version of code ran the operation.

.. _hook_triggers:

Hook Triggers
=============

The following triggers are provided:
1. :py:meth:`~flow.FlowProject.add_hook.on_start` will execute when the operation begins execution.
2. :py:meth:`~flow.FlowProject.add_hook.on_exit` will execute when the operation exits, with or without error.
3. :py:meth:`~flow.FlowProject.add_hook.on_success` will execute when the operation exits without error.
4. :py:meth:`~flow.FlowProject.add_hook.on_error` will execute when the operation exits with error.

Hooks can be installed at the :ref:`operation level <operation hooks>` or at the :ref:`flow-project level<project-level hooks>`.
Project-level hooks are called for every operation in the flow project.

.. note::

    Hooks are run in the environment of the python process from which you call **flow**.
    For this reason, hooks will not have access to modules in a container if you use that as your execution directive.

.. _operation hooks:

Operation Hooks
===============

Hooks may be added to individual operations using decorators.
The :py:class:`~flow.FlowProject.add_hook` decorator tells :py:class:`~signac` to run a hook (or set of hooks) when an operation reaches the specified trigger.

The :py:class:`~flow.FlowProject.add_hook` decorator accepts objects as a function of the job operation (:py:class:`~flow.project.JobOperation`).
The decorators :py:meth:`~flow.FlowProject.add_hook.on_start` and  :py:meth:`~flow.FlowProject.add_hook.on_exit` accept functions with two parameters: the operation name and the :py:class:`Job` object.
The decorator :py:meth:`~flow.FlowProject.add_hook.on_error`, accepts functions with three parameters: the operation name, the output error, and the :py:class:`Job` object.

:py:class:`~flow.FlowProject.add_hook` can be used to store basic information about the execution of a job operation in the job document.

In the following example, either the function ``store_success_to_doc`` executes after the :py:class:`~flow.project.JobOperation`, ``foo``, exits without error, or ``store_error_to_doc`` executes after ``foo`` exits with error:

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
    @FlowProject.add_hook.on_error(store_error_to_doc)
    @FlowProject.post.isfile("result.txt")
    def foo(job):
        if job.sp.a == 0:
            # Have jobs with statepoint 'a' == 0 fail
            raise ValueError

    if __name__ == '__main__':
       FlowProject().main()

If ``foo`` is executed using ``python project.py run -o foo -f a 1``, the hook triggered ``on_success`` will run, and `job.doc.foo_success` will be ``True``.

If ``foo`` is executed using ``python project.py run -o foo -f a 0``, a ``ValueError`` is raised.
The hook triggered ``on_error`` will run, and ``job.doc.foo_success`` will be ``False``.

.. note::

    Unlike :py:meth:`~flow.FlowProject.add_hook.on_start`, :py:meth:`~flow.FlowProject.add_hook.on_exit`,  and :py:meth:`~flow.FlowProject.add_hook.on_success`, which accept functions that take ``operation_name`` and ``job`` as arguments, :py:meth:`~flow.FlowProject.add_hook.on_error` accepts functions that take ``operation_name``, ``error``, and ``job`` as arguments.

.. _project-level hooks:

Project-Level Hooks
===================

In some cases, it may be desirable to install the same hook or set of hooks for all operations in a project.
For example, to create a project level hook that sets a job document key, ``f"{operation_name}_start"`` to ``True`` at the start of execution:

 .. code-block:: python

    # project.py
    from flow import FlowProject #etc


    class Project(FlowProject):
        pass


    def track_start(operation_name, job):
        job.doc[f"{operation_name}_start"] = True


    if __name__ == '__main__':
        project = Project()
        project.hooks.on_start.append(track_start)
        project.main()


A custom set of hooks may also be installed by a custom ``install_hooks`` method:

.. code-block:: python

    # project.py
    from flow import FlowProject #etc

    class Project(FlowProject):
        pass

    ...  # Define various job operations


    # Define custom hooks class. This can be done in a seperate file and imported into the project.py file.
    class ProjectHooks:

        def __init__(self, project):
            self.project = project

        def set_job_doc(self, key):
            def set_true(operation_name, job):
                job.doc[f"{operation_name}_{key}"] = True
            return set_true

        def set_job_doc_with_error(self):
            def set_false(operation_name, error, job):
                job.doc[f"{operation_name}_success"] = True
            return set_false

        def install_hooks(self):
            self.project.hooks.on_start.append(set_job_doc("start"))
            self.project.hooks.on_success.append(set_job_doc("success"))
            self.project.hooks.on_error.append(set_job_doc_with_error())
            return self.project


    if __name__ == '__main__':
        project = Project()
        ProjectHooks(project).main()
