# How to Contribute to the Project

## Providing Feedback

Issue reports and feature proposals are very welcome.
Please use the [GitHub issue page](https://github.com/glotzerlab/signac-docs/issues/) for this.

## Writing Documentation

The API of each package as part of the framework is documented in the form of doc-strings, which are published on https://signac.readthedocs.io/projects/$package, where `$package` is currently one of `core`, `flow`, or `dashboard`.
A more general introduction in the form of tutorials, guides, and recipes is published as part of the framework documentation: https://signac.readthedocs.io.

Anyone is invited to add to or edit any part of the documentation.
To fix a spelling mistake or to make a minor edits, just click on the **Edit on GitHub** button in the top-right corner.
We recommend to clone the signac-docs repository for more substantial edits on your local machine.

## Contributing Code

Code contributions to the signac-docs open-source project are welcomed via pull requests on GitHub.
Prior any work you should contact the signac developers to ensure that the planned development meshes well with the directions and standards of the project.
All contributors must agree to the Contributor Agreement ([ContributorAgreement.md](ContributorAgreement.md)) before their pull request can be merged.

### Guideline for Code Contributions

  * Use the [OneFlow](https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow) model of development:
    - Both new features and bug fixes should be developed in branches based on `main`.
    - Hotfixes (critical bugs that need to be released *fast*) should be developed in a branch based on the latest tagged release.
  * Write code that is compatible with all supported versions of Python (listed in [pyproject.toml](https://github.com/glotzerlab/signac/blob/main/pyproject.toml)).
  * Avoid introducing dependencies -- especially those that might be harder to install in high-performance computing environments.
  * Create [unit tests](https://en.wikipedia.org/wiki/Unit_testing) and [integration tests](https://en.wikipedia.org/wiki/Integration_testing) that cover the common cases and the corner cases of the code.
  * Preserve backwards-compatibility whenever possible, and make clear if something must change.
  * Document any portions of the code that might be less clear to others, especially to new developers.
  * Write API documentation in this package, and put usage information, guides, and concept overviews in the [framework documentation](https://signac.readthedocs.io/) ([source](https://github.com/glotzerlab/signac-docs/)).

Please see the [Support](https://signac.readthedocs.io/projects/core/en/latest/support.html) section as part of the documentation for detailed development guidelines.

### Code style

Code submitted to the signac-docs project must adhere to the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/) with the exception that lines may have up to 100 characters.

We recommend to use [flake8](http://flake8.pycqa.org/en/latest/) and [autopep8](https://pypi.org/project/autopep8/) to find and fix any code style issues prior to committing and pushing.

## Reviewing Pull Requests

Pull requests represent the standard way of contributing code to the code base.
Each pull request is assigned to one of the maintainers, who is responsible for triaging it, finding at least two reviewers (one of them can be themselves), and to eventually merge or decline it.
Pull requests should generally be approved by two reviewers prior to merge.

### Guideline for pull request reviewers

The following items represent a general guideline for points that should be considered during the review process:

* Breaking changes to the API should be avoided whenever possible and require approval by a lead maintainer.
* Significant performance degradations must be avoided unless the regression is necessary to fix a bug.
* Updates for non-trivial bug fixes should be accompanied by a unit test that catches the related issue to avoid future regression.
* The code is easy to follow and sufficiently documented to be understandable even to developers who are not highly familiar with the code.
* Code duplication should be avoided and existing classes and functions are effectively reused.
* The pull request is on-topic and does not introduce multiple independent changes (e.g. unrelated style fixes etc.).
* A potential increase in code complexity introduced with this update is well justified by the benefits of the added feature.
* The API of a new feature is well-documented in the doc-strings and usage is documented as part of the [framework documentation](https://github.com/glotzerlab/signac-docs).
