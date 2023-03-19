.. _configuration:

=============
Configuration
=============

Overview
========

The **signac** framework is configured with configuration files.
The configuration files are stored using the standard `INI file format <https://en.wikipedia.org/wiki/INI_file>`__.
In general, two config files are supported:

  1. Project-specific configuration uses the ``.signac/config`` file at the project root directory.
  3. Per-user configuration is stored in a global file at ``$HOME/.signacrc``.

You can either edit these configuration files manually, or execute ``signac config`` on the command line.
Please see ``signac config --help`` for more information.

Project configuration
=====================

A project configuration file is defined as a file named ``config`` contained within a ``.signac`` directory.
Functions like :py:func:`~signac.get_project` will search upwards from a provided directory until a project configuration is found to indicate the project root.
This is an example for a project configuration file:

.. code-block:: ini

   # signac.rc
   schema_version = 2

schema_version
  Identifier for the current internal schema used by signac. This schema version determines internal details such as the location of configuration files or caches.
