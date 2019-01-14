.. _environments:

===================
Manage Environments
===================

The **signac-flow** package uses environment profiles to adjust the submission process to local environments.
That is because different environments provide different resources and options for the submission of operations to those resources.
Although the basic options will always be the same, there might be some subtle differences depending on where you want to submit your operations.

.. tip::

    If you are running on a high-performance super computer, add the following line to your ``project.py`` module to import packaged profiles: ``import flow.environments``
    Please see :ref:`supported-environments` for more information.

How to Use Environments
=======================

Environments are defined by subclassing from the :py:class:`~flow.ComputeEnvironment` class.
The :py:class:`~flow.ComputeEnvironment` class is a *meta-class* that ensures that all subclasses are automatically globally registered when they are defined.
This enables us to use environments simply by defining them or importing them from a different module.
The :py:func:`flow.get_environment` function will go through all defined :py:class:`~flow.ComputeEnvironment` classes and return the one where the :py:meth:`~flow.ComputeEnvironment.is_present` class method returns ``True``.

Packaged Environments
=====================

The package comes with a few *default environments* which are **always available** and designed for specific schedulers.
That includes the :py:class:`~flow.DefaultTorqueEnvironment` and the :py:class:`~flow.DefaultSlurmEnvironment`.
This means that if you are within an environment with a *torque* or *slurm scheduler* you should be immediately able to submit to the cluster.

In addition, **signac-flow** comes with some environments tailored to specific compute clusters that are defined in the :py:mod:`flow.environments` module.
These environments are not automatically available.
Instead, you need to *explictly import* the :py:mod:`flow.environments` module.

For a full list of all packaged environments, please see :ref:`supported-environments`.

Defining New Environments
=========================

In order to implement a new environment, create a new class that inherits from :py:class:`flow.ComputeEnvironment`.
You will need to define a detection algorithm for your environment, by default we use a regular expression that matches the return value of :py:func:`socket.getfqdn()`.

Those are the steps usually required to define a new environment:

  1. Subclass from :py:class:`flow.ComputeEnvironment`.
  2. Determine a `regular expression <https://en.wikipedia.org/wiki/Regular_expression>`_ that would match the output of :py:func:`socket.getfqdn()`.
  3. Create a template and specify the template name as ``template`` class variable.

This is an example for a typical environment class definition:

.. code-block:: python

      class MyUniversityCluster(flow.DefaultTorqueEnvironment):

          hostname_pattern = r'.*\.mycluster\.university\.edu$'  # Matches names like login.mycluster.university.edu
          template = 'mycluster.myuniversity.sh'

Then, add the ``mycluster.myuniversity.sh`` template script to the ``templates/`` directory within your project root directory.

.. important::

    The new environment will be automatically registered and used as long as it is either defined within the same module as your :py:class:`~flow.flow.FlowProject` class or its module is imported into the same module.

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
While there are a few steps, they are almost all entirely automated, with the exception of actually reviewing the scripts your environment generates.
Once you've written the environment class and the template as described above, contributing the environments to the package involves the following:

  1. Create a new branch of **signac-flow** based on the *develop* branch.
  2. Add your environment class to the *flow/environments/* directory, and add the corresponding template to the *flow/templates/* directory.
  3. Run the `tests/test_templates.py` test script. It should fail on your environment, indicating that no reference scripts exist yet.
  4. Update the `environments` dictionary in the `init` function of `tests/generate_template_reference_data.py`. The dictionary indicates the submission argument combinations that need to be tested for your environment.
  5. Run the `tests/generate_template_reference_data.py` script, which will create the appropriate reference data in the `tests/template_reference_data.tar.gz` tarball based on your modifications. The `test_templates.py` script should now succeed.
  6. Run the `tests/extract_templates.py` script, which will extract the tarball into a **signac** project folder.
  7. Run the `tests/generate_template_review_document.py` script, which will generate docx files in the *tests/compiled_scripts/* directory, one for each environment.
  8. You should see one named after your new environment class. **Review the generated scripts thoroughly.** This step is critical, as it ensures that the environment is correctly generating scripts for various types of submission.
  9. Once you've fixed any issues with your environment and template, push your changes and create a pull request. You're done!
