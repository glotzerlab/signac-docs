
Community
=========

.. _numfocus:

NumFOCUS
--------

The signac framework is part of the community of `NumFOCUS Affiliated Projects <https://numfocus.org/sponsored-projects/affiliated-projects>`_.

.. _conduct:

Code of Conduct
---------------

All community members are expected to follow the signac project's `code of conduct <https://signac.readthedocs.io/conduct/>`_.

.. _support:

Support
-------

The signac community offers user support and communicates about code development through `GitHub Discussions`_ and the `Slack workspace`_.

Please use the issue trackers of the individual :ref:`packages <package-overview>` to file bug reports or request new features!

Developer meetings are open to the community. The signac Google Calendar is publicly available at this `iCal link`_.
The Google Calendar is also embedded below:

.. raw:: html

    <iframe
        src="https://calendar.google.com/calendar/embed?src=6pfj3imrfa87i29icmm93f3mi8%40group.calendar.google.com"
        style="border: 0" width="700" height="450" frameborder="0" scrolling="no">
    </iframe>


.. _GitHub Discussions: https://github.com/glotzerlab/signac/discussions
.. _Slack workspace: https://signac.readthedocs.io/slack-invite/
.. _iCal link: https://calendar.google.com/calendar/ical/6pfj3imrfa87i29icmm93f3mi8%40group.calendar.google.com/public/basic.ics

.. _contribute:

Contributions
-------------

Contributions to **signac** are very welcome!
We highly appreciate contributions in the form of **user feedback** and **bug reports**.
Such contributions are best communicated through our `Slack workspace`_, or the issue trackers or GitHub Discussions of individual :ref:`packages <package-overview>`.
Developers are invited to contribute to the framework by pull request to the appropriate package repository.
The source code for all packages is hosted on `GitHub`_.
We recommend discussing new features in form of a proposal on the issue tracker for the appropriate project prior to development.

All code contributed via pull request needs to adhere to the following guidelines:

  * Use the `OneFlow`_ model of development:

    - Both new features and bug fixes should be developed in branches based on ``main``.
    - Hotfixes (critical bugs that need to be released *fast*) should be developed in a branch based on the latest tagged release.

  * Write code that is compatible with all supported versions of Python (listed in the package ``pyproject.toml`` file).
  * Avoid introducing dependencies -- especially those that might be harder to install in high-performance computing environments.
  * All code needs to adhere to the PEP8_ style guide, with the exception that a line may have up to 100 characters.
  * Create `unit tests <https://en.wikipedia.org/wiki/Unit_testing>`_  and `integration tests <ttps://en.wikipedia.org/wiki/Integration_testing>`_ that cover the common cases and the corner cases of the code.
  * Preserve backwards compatibility whenever possible, and make clear if something must change.
  * Document any portions of the code that might be less clear to others, especially to new developers.
  * Write API documentation as part of the docstrings of the package, and put usage information, guides, and concept overviews in the `framework documentation <https://signac.readthedocs.io/>`_, the page you are currently on (`source <https://github.com/glotzerlab/signac-docs/>`_).

.. _GitHub: https://github.com/glotzerlab/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _OneFlow: https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow

.. tip::

    During continuous integration, the code and the documentation are formatted and checked automatically using `black`_, `isort`_, `flake8`_, `pydocstyle`_, and `mypy`_.
    These tools ensure high code quality, establish project standards, and reduce the number of iterations needed in the code review process.
    Run the following commands to set up a pre-commit hook, using the tool `pre-commit`_, that will ensure your code and documentation are compliant before committing:

    .. code-block:: bash

        pip install pre-commit
        pre-commit install

    To install and run `Pre-commit`_ for all the files present in the repository, run the following command:

    .. code-block:: bash

        pre-commit run --all-files

.. _black: https://black.readthedocs.io/en/stable/
.. _isort: https://pycqa.github.io/isort/
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _pydocstyle: http://www.pydocstyle.org/en/stable/
.. _mypy: https://mypy.readthedocs.io/en/stable/
.. _pre-commit: https://pre-commit.com/

.. note::

    Please see the individual package documentation for detailed guidelines on how to contribute to a specific package.
