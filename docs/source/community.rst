
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
The source code for all packages is hosted on `github`_.
We recommend discussing new features in form of a proposal on the issue tracker for the appropriate project prior to development.

All code contributed via pull request needs to adhere to the following guidelines:

  * Use the OneFlow_ model of development:
    - Both new features and bug fixes should be developed in branches based on ``master``.
    - Hotfixes (critical bugs that need to be released *fast*) should be developed in a branch based on the latest tagged release.
  * Write code that is compatible with all supported versions of Python (listed in the package ``setup.py`` file).
  * Avoid introducing dependencies -- especially those that might be harder to install in high-performance computing environments.     
  * All code needs to adhere to the PEP8_ style guide, with the exception that a line may have up to 100 characters.
  * Create `unit tests <https://en.wikipedia.org/wiki/Unit_testing>`_  and `integration tests <ttps://en.wikipedia.org/wiki/Integration_testing>`_ that cover the common cases and the corner cases of the code.
  * Preserve backwards-compatibility whenever possible, and make clear if something must change.
  * Document any portions of the code that might be less clear to others, especially to new developers.
  * Write API documentation as part of the doc-strings of the package, and put usage information, guides, and concept overviews in the `framework documentation <https://docs.signac.io/>`_, the page you are currently on (`source <https://github.com/glotzerlab/signac-docs/>`_).

.. _github: https://github.com/glotzerlab/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _OneFlow: https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow

.. tip::

    During continuous integration, the code is checked automatically with `Flake8`_.
    Run the following commands to set up a pre-commit hook that will ensure your code is compliant before committing:

    .. code-block:: bash

        flake8 --install-hook git
        git config --bool flake8.strict true


.. _Flake8: http://flake8.pycqa.org/en/latest/

.. note::

    Please see the individual package documentation for detailed guidelines on how to contribute to a specific package.
