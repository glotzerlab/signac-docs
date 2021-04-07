.. _templates:

=========
Templates
=========

The **signac-flow** package uses jinja2_ templates to generate scripts for execution and submission to cluster scheduling systems.
Templates for simple bash execution and submission to popular schedulers and compute clusters are shipped with the package.
To customize the script generation, a user can replace the default template or customize any of the provided ones.

.. _jinja2: http://jinja.pocoo.org/

Replacing the default template
==============================

The default ``script.sh`` template simply extends from another script according to the ``base_script`` variable, which is dynamically set by **signac-flow**:

.. code-block:: jinja

    {% extends base_script %}

This ``base_script`` variable provides a way to inject specific templates for, *e.g.*, different environments.
However, by default any templates placed within your project root directory in a file called ``templates/script.sh`` will be used instead of the defaults provided by **signac-flow**.
This makes it easy to completely replace the scripts provided by signac-flow; to use your own custom script, simply place a new ``script.sh`` in a ``templates`` directory within your project root directory.
This is an example for a basic template that would be sufficient for the simple serial execution of multiple operations:

.. code-block:: jinja

    cd {{ project.config.project_dir }}

    {% for operation in operations %}
    {{ operation.cmd }}
    {% endfor %}


Customize provided templates
============================

Instead of simply replacing the template as shown above, we can also customize the provided templates.
One major advantage is that we can still use the template scripts for cluster submission.

Assuming that we wanted to write a time stamp to some log file before executing operations, we could provide a custom template such as this one:

.. code-block:: jinja

    {% extends base_script %}
    {% block body %}
    date >> execution.log
    {{ super() }}
    {% endblock %}

The first line again indicates that this template extends an existing template based on the value of ``base_script``; how this variable is set is explained in more detail in the next section.
The second and last line indicate that the enclosed lines are to be placed in the *body* block of the base template.
The third line is the actual command that we want to add and the fourth line ensures that the code provided by the base template within the body block is still added.

The base template
=================

The **signac-flow** package will select a different base script template depending on whether you are simply generating a script using the ``script`` command or whether you are submitting to a scheduling system with ``submit``.
In the latter case, the base script template is selected based on whether you are on any of the :ref:`officially supported environments <supported-environments>`, and if not, whether one of the known scheduling systems (e.g. Slurm, PBS, or LSF) is available.
This is a short illustration of that heuristic:

.. code-block:: bash

    # The `script` command always uses the same base script template:
    project.py script --> base_script='base_script.sh'

    # On system with SLURM scheduler:
    project.py submit --> base_script='slurm.sh' (extends 'base_script.sh')

    # On XSEDE Comet
    project.py submit --> base_script='comet.sh' (extends 'slurm.sh')

Regardless of which *base script template* you are actually extending from, all templates shipped with **flow** follow the same basic structure:

.. glossary::

   resources
    Calculation of the total resources required for the execution of this (submission) script.

   header
    Directives for the scheduling system such as the cluster job name and required resources.
    This block is empty for shell script templates.

   project_header
    Commands that should be executed once before the execution of operations, such as switching into the project root directory or setting up the software environment.

   body
    All commands required for the actual execution of operations.

   footer
    Any commands that should be executed at the very end of the script.
