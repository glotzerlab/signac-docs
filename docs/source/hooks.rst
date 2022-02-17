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
called triggers.

For example, operation failures may be tracked in the job document as `job.doc['operation_success'] = False`,
while operation successes may be tracked in the job document as `job.doc['operation_success'] = True`.

Hooks help track where an execution's data originated, and which operations were applied to the data.
For examples, users may record the `git commit ID <https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History>`_ upon execution of an operation,
allowing users to track which version of code was used to run the operation.

Hooks can be installed at the :ref:`operation level <operation hooks>`
or at the :ref:`flow-project level<project-level hooks>`, as shown below.
Project-level hooks are called for every operation in the flow project.

.. note::

    Hooks are run in the environment of the python process from which you call **flow**.
    For this reason,
    hooks will not have access to modules in a container if you use that as your execution directive.

.. _operation hooks:

Operation Hooks
===============

Hooks may be added to individual operations using decorators.
The :py:class:`~flow.FlowProject.add_hook` decorator tells :py:class:`~signac` to run a
hook (or set of hooks) when an operation reaches any of the following triggers:
    * :py:meth:`~flow.FlowProject.add_hook.on_start` will execute when the operation begins execution.
    * :py:meth:`~flow.FlowProject.add_hook.on_finish` will execute when the operation exits, with or without error.
    * :py:meth:`~flow.FlowProject.add_hook.on_success` will execute when the operation exits without error.
    * :py:meth:`~flow.FlowProject.add_hook.on_fail` will execute when the operation exits with error.

The :py:class:`~flow.FlowProject.add_hook` decorator accepts objects as a function of the job operation
(:py:class:`~flow.project.JobOperation`).
The decorators :py:meth:`~flow.FlowProject.add_hook.on_start` and  :py:meth:`~flow.FlowProject.add_hook.on_finish`
accept functions with two parameters: the operation name and the :py:class:`Job` object.
The decorator :py:meth:`~flow.FlowProject.add_hook.on_fail`, accepts functions with three parameters: the operation name, the output error,
and the :py:class:`Job` object.

:py:class:`~flow.FlowProject.add_hook` can be used to store basic information about the execution of a job operation in the job document.

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
and `job.doc.foo_success` will be ``True``.

If ``foo`` is executed using ``python project.py run -o foo -f a 0``, a ``ValueError`` is raised.
The hook triggered ``on_fail`` will run, and ``job.doc.foo_success`` will be ``False``.

.. note::

    Unlike :py:meth:`~flow.FlowProject.add_hook.on_start`, :py:meth:`~flow.FlowProject.add_hook.on_finish`,
    and :py:meth:`~flow.FlowProject.add_hook.on_success`,
    which accept functions that take ``operation_name`` and ``job`` as arguments,
    :py:meth:`~flow.FlowProject.add_hook.on_fail` accepts functions that take ``operation_name``, ``error``,
    and ``job`` as arguments.

.. _project-level hooks:

Project-Level Hooks
===================

In some cases, it may be desirable to install the same hook or set of hooks for all operations in a project.
For example, to create a  project level hook that sets a job document key, ``f"{operation_name}_start"`` to ``True`` at the start of execution:
 
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
            self.project.hooks.on_fail.append(set_job_doc_with_error())
            return self.project

    
    if __name__ == '__main__':
        project = Project()
        ProjectHooks(project).main()

