
Community
=========

.. _support:

Chat Support
------------

To best way to get support for **signac** is to join the `signac-gitter channel <https://gitter.im/signac/Lobby>`_.
The developers and other users are usually able to help within a few minutes.
Alternatively, you can send an email to signac-support@umich.edu.

Please use the issue tracker of the individual :ref:`packages <package-overview>` to file bug reports or request new features!

.. _contribute:

Contributions
-------------

Contributions to **signac** are very welcome!
We highly appreciate contributions in the form of **user feedback** and **bug reports** on the `gitter channel <https://gitter.im/signac/Lobby>`_, the issue trackers of individual :ref:`packages <package-overview>`, or via `email <mailto:signac-support@umichedu>`_.
Developers are invited to contribute to the framework by pull request to the appropriate package repository.
The source code for all packages is hosted on `bitbucket`_.
We recommend discussing new features in form of a proposal on the issue tracker for the appropriate project prior to development.

All code contributed via pull request needs to adhere to the following guidelines:

  1. Most signac packages follow the `git-flow`_ branching model.
     Bug fixes should be implemented in a branch based on ``master``, while new features should be developed within a branch based on ``develop``.
  2. All code needs to adhere to the `PEP8`_ style guide, with the exception that a line may have up to 100 characters.
  3. New features must be properly documented and tested with automated unit tests.
  4. Non-obvious code passages should be extensively documented.
  5. Changes must generally be backwards-compatible.
  6. All packages targeted to be used within high-performance computing environments should support Python versions 2.7+ and 3.4+ and keep the number of *hard* dependencies to a miminum.

.. _bitbucket: https://bitbucket.org/account/user/glotzer/projects/SIG
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _git-flow: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

.. tip::

    During continuous integration, the code is checked automatically with `Flake8`_.
    Run the following commands to set up a pre-commit hook that will ensure your code is compliant before committing:

    .. code-block:: bash

        flake8 --install-hook git
        git config --bool flake8.strict true


.. _Flake8: http://flake8.pycqa.org/en/latest/

.. note::

    Please see the individual package documentation for detailed guidelines on how to contribute to a specific package.
