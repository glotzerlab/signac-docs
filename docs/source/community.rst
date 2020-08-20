
Community
=========

.. _numfocus:

NumFOCUS
--------

The signac framework is part of the community of `NumFOCUS Affiliated Projects <https://numfocus.org/sponsored-projects/affiliated-projects>`_.

.. _conduct:

Code of Conduct
---------------

All community members are expected to follow the signac project's `code of conduct <https://signac.io/conduct/>`_.

.. _support:

Support
-------

The signac community offers real-time user support through the `signac gitter chat room <https://gitter.im/signac/Lobby>`_ and `Slack workspace`_.
The project's primary communication channel for code development is the Slack workspace.
Alternatively, you can send an email to `signac-support@umich.edu <signac-support@umich.edu>`_.

Please use the issue trackers of the individual :ref:`packages <package-overview>` to file bug reports or request new features!

.. _gitter: https://gitter.im/signac/Lobby
.. _Slack workspace: https://join.slack.com/t/signac/shared_invite/enQtNzk2MTUxNjU5ODkzLWM1NDFmMzRmMTA2MjFlN2ZiOTQ4MDBjNmIwMmM4YTgyZTQ1ODFkMGNhZTc5M2IwMmE1MWJiOTliN2Y2Y2M3ZDY

.. _contribute:

Contributions
-------------

Contributions to **signac** are very welcome!
We highly appreciate contributions in the form of **user feedback** and **bug reports**.
Such contributions are best communicated through our `Slack workspace`_, which we use for developer discussions, the issue trackers of individual :ref:`packages <package-overview>`, or via `email <signac-support@umich.edu>`_.
Developers are invited to contribute to the framework by pull request to the appropriate package repository.
The source code for all packages is hosted on `GitHub`_.
We recommend discussing new features in form of a proposal on the issue tracker for the appropriate project prior to development.

All code contributed via pull request needs to adhere to the following guidelines:

  * Use the `OneFlow`_ model of development:

    - Both new features and bug fixes should be developed in branches based on ``master``.
    - Hotfixes (critical bugs that need to be released *fast*) should be developed in a branch based on the latest tagged release.

  * Write code that is compatible with all supported versions of Python (listed in the package ``setup.py`` file).
  * Avoid introducing dependencies -- especially those that might be harder to install in high-performance computing environments.
  * All code needs to adhere to the PEP8_ style guide, with the exception that a line may have up to 100 characters.
  * Create `unit tests <https://en.wikipedia.org/wiki/Unit_testing>`_  and `integration tests <ttps://en.wikipedia.org/wiki/Integration_testing>`_ that cover the common cases and the corner cases of the code.
  * Preserve backwards-compatibility whenever possible, and make clear if something must change.
  * Document any portions of the code that might be less clear to others, especially to new developers.
  * Write API documentation as part of the doc-strings of the package, and put usage information, guides, and concept overviews in the `framework documentation <https://docs.signac.io/>`_, the page you are currently on (`source <https://github.com/glotzerlab/signac-docs/>`_).

.. _GitHub: https://github.com/glotzerlab/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _OneFlow: https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow

.. tip::

    During continuous integration, the code and the documentation is checked automatically using `Flake8`_, `Pydocstyle`_, and `Mypy`_.
    Run the following commands to set up a pre-commit hook, using `Pre-commit`_, that will ensure your code and documentation are compliant before committing:

    .. code-block:: bash

        pip install -r requirements-precommit.txt
        pre-commit install

    To install and run `Pre-commit`_ for all the files present in the repository, run the following command:

    .. code-block:: bash

        pre-commit run --all-files

.. _Flake8: https://flake8.pycqa.org/en/latest/
.. _Pydocstyle: http://pydocstyle.org/en/4.0.0/index.html
.. _Mypy: https://mypy.readthedocs.io/en/stable/
.. _Pre-commit: https://pre-commit.com/

.. note::

    **signac** and **signac-flow** uses specific versions of the dependencies for setting up a pre-commit hook. Please see the file ``requirements-precommit.txt`` of both the repositories for more details.
    Please see the individual package documentation for detailed guidelines on how to contribute to a specific package.
