.. _environments:

===================
Manage Environments
===================

The **signac-flow** package uses environment profiles to adjust the submission process to local environments.
That is because different environments provide different resources and options for the submission of operations to those resources.
Although the basic options will always be the same, there might be some subtle differences depending on where you want to submit your operations.

How to Use Environments
=======================

Environments are defined by subclassing from the :py:class:`~flow.environment.ComputeEnvironment` class.
The :py:class:`~flow.environment.ComputeEnvironment` class is a *meta-class* that ensures that all subclasses are automatically globally registered when they are defined.
This enables us to use environments simply by defining them or importing them from a different module.
The :py:func:`flow.get_environment` function will go through all defined :py:class:`~flow.environment.ComputeEnvironment` classes and return the one where the :py:meth:`~flow.environment.ComputeEnvironment.is_present` class method returns ``True``.

Packaged Environments
=====================

The package comes with a few *default environments* which are **always available** and designed for specific schedulers.
That includes the :py:class:`~flow.environment.DefaultPBSEnvironment` and the :py:class:`~flow.environment.DefaultSlurmEnvironment`.
This means that if you are within an environment with a *PBS* or *Slurm scheduler* you should be immediately able to submit to the cluster.

In addition, **signac-flow** comes with some environments tailored to specific compute clusters that are defined in the :py:mod:`flow.environments` module.
These environments are also automatically available, but if they conflict with a specific environment of your choice, you can opt out of using these environments by setting the ``flow.import_packaged_environments`` signac config variable.
For instance, to opt out of using these environments for a specific signac project, execute ``signac config set flow.import_packaged_environments off`` within that environment.
This variable may also be set within the global signac configuration file on a given cluster.
More generally, if you simply wish to force **signac-flow** to use a particular environment, you may do so by setting the environment variable ``SIGNAC_FLOW_ENVIRONMENT`` in your shell.

For a full list of all packaged environments, please see :ref:`supported-environments`.

Defining New Environments
=========================

In order to implement a new environment, create a new class that inherits from :py:class:`flow.environment.ComputeEnvironment`.
You will need to define a detection algorithm for your environment, by default we use a regular expression that matches the return value of :py:func:`socket.getfqdn()`.

Those are the steps usually required to define a new environment:

  1. Subclass from :py:class:`flow.environment.ComputeEnvironment`.
  2. Determine a `regular expression <https://en.wikipedia.org/wiki/Regular_expression>`_ that would match the output of :py:func:`socket.getfqdn()`.
  3. Create a template and specify the template name as ``template`` class variable.

This is an example for a typical environment class definition:

.. code-block:: python

      class MyUniversityCluster(flow.environment.DefaultSlurmEnvironment):

          hostname_pattern = r'.*\.mycluster\.university\.edu$'  # Matches names like login.mycluster.university.edu
          template = 'myuniversity-mycluster.sh'

Then, add the ``myuniversity-mycluster.sh`` template script to the ``templates/`` directory within your project root directory.

.. important::

    The new environment will be automatically registered and used as long as it is either defined within the same module as your :py:class:`~flow.FlowProject` class or its module is imported into the same module.

As an example on how to write a submission script template, this would be a viable template to define the header for a SLURM scheduler:

.. code-block:: jinja

    {% extends "base_script.sh" %}
    {% block header %}
    #!/bin/bash
    #SBATCH --job-name="{{ id }}"
    #SBATCH --partition={{ partition }}
    #SBATCH -t {{ walltime|format_timedelta }}
    {% block tasks %}
    #SBATCH --ntasks={{ np_global }}
    {% endblock %}
    {% endblock %}


All templates, which are shipped with the package, are within the *flow/templates/* directory within the package source code.


Contributing Environments to the Package
========================================

Users are **highly encouraged** to contribute environment profiles that they developed for their local environments.
In order to contribute an environment, either simply email them to the package maintainers (see the README for contact information) or create a pull request.
