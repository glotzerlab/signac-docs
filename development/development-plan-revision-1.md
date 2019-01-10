# Development Plan for Revision 1.0

**Authors**

* Carl Simon Adorf (csadorf@umich.edu)

## About

This document describes the development plan for the implementation of design specifications for signac (core) **revision 1** and is maintained by the signac core maintainers.
The development plan will be continually updated to account for changes and refinements during the execution of this process.

**Targeted audience**

* Core maintainers

## Phase 1 (Planning)

The initial phase is targeted at deciding on the general concept and API for revision 1 as well as setting up a developer team and obtaining general buy-in by expert users.

### Executed by

* Core maintainers

### Steps

1. Refine design specifications until consensus among maintainers is reached.
1. Determine developer team candidate pool and communication channels for outreach.
1. Reach out to candidate developers and users to aggregate a team of people who are interested in contributing by:
 * contributing code
 * writing documentation
 * testing code
 * providing feedback
1. Consider the implementation of an advisory board constituted by experts in the field who advise the core development team on
 * the design specification,
 * the planning and execution of development,
 * publication and outreach activities.
1. Consider to switch development platform based on tentative developer team composition.
1. Create branch *revision-1* based off *master*.
1. Implement a single minimal module that demonstrates code and documentation style for developers approved by maintainers.
1. Implement a minimal test module that demonstrates use of the testing framework approved by maintainers.
1. Setup development guidelines approved by maintainers.
1. Identify work packages to be assigned to tentative developer team.

*All steps are executed in parallel, but are roughly ordered by priority.*

### Deliverables

* A maintainer-approved revision of the design specifications.
* A tentative developer team.
* A list of users who are willing to provide feedback and conduct alpha- and beta-testing.
* Minimal module for revised interface.
* Minimal test module for revised interface.
* Development guidelines.
* Work packages for tentative developer team

## Phase 2 (Pre-Alpha)

This phase is targeted at setting up the development workflow and creating an early prototype which can be used to refine the design specifications.

### Executed by

* Core maintainers
* Development team
* Interested users

### Steps

1. Refine design specifications until consensus among maintainers is reached.
1. Implement unit and integration tests for interface described in the design specifications.

    * Write completely separate test modules, but copy & paste code liberally from the current code base as needed.

1. Implement prototype interfaces as described in the design specifications.

    * Implement new classes in completely separate modules and rename existing modules in case of name clashes.
    * Copy & paste code liberally from current code base as needed.
    * Rename existing classes as needed, but create an alias in place.
    * Do not extend existing classes, instead rename them in case of name clashes.
    * Write only basic documentation as part of the doc-strings.

1. Create a conceptual outline of the overall revised user documentation; doc-strings and the design specifications serve as user documentation at this point.

1. Develop a plan on obtaining backwards-compatibility including a deprecation schedule. Prototype implementations may be implemented where constructive and feasible.

1. Create tagged revision *revision-1-pre-alpha*.

1. Conduct online focus group session on prototype implementation.

*Steps 2-5 are executed in parallel.*

### Deliverables

 * Prototype implementation that allows execution of API examples shown in the design specifications.
 * Essential unit and integration tests for revised API pass. Which tests are deemed essential will be decided by the maintainers at a later stage.
 * Basic outline of the user documentation.
 * Basic plan on how to maintain backwards compatibility with versions 0.9+.
 * Feedback from users and developers on prototype implementation.

## Phase 3 (Alpha)

This phase is targeted at creating an alpha-version that is fully compliant with the specifications, and has a partially complete automated testing framework.

### Executed by

* Core maintainers
* Development team
* Alpha-testers

This phase is targeted at polishing the design specifications and revised API, developing  user documentation, and developing prototypes to obtain backwards compatibility.

### Steps

1. Create new revision of the design specifications taking into account feedback gathered during phase 2 and refine until consensus is reached among maintainers.
1. Update prototypes and tests with revised design specifications.
1. The doc-string documentation is extended where needed.
1. Draft a revised version of the overall user documentation.
1. Create tagged revision *revision-1-alpha*.
1. Obtain feedback from alpha-testers.

*Steps 2-4 are executed in parallel.*

### Deliverables

* Revised design specifications.
* Full implementation of revised API.
* Full implementation of all unit and integration tests for revised API.
* Feedback from alpha-testers.

## Phase 4 (Beta)

This phase is targeted at creating a largely bug-free beta-version that is fully compliant with the specifications, fully backwards compatible, and has a complete automated test framework.
Furthermore, this version will be used during beta testing to identify any latent issues with the revised API in preparation for the creation of release candidate 1.

## Executed by

* Core maintainers
* Development team
* Beta-testers

### Steps

1. Create new revision of the design specification taking into account feedback gathered during phase 3 and refine until consensus is reached among maintainers.
1. Update implementation and tests with revised design specifications.
1. Implement compatibility layers necessary to obtain full backwards compatibility.

    Full compatibility may not be possible to achieve in some cases. The core maintainers will decide which tests can be changed or removed.

1. Complete and refine the user documentation on revised API.
1. Create tagged revision *revision-1-beta*.
1. Obtain feedback from beta-testers.

*Steps 2-4 are executed in parallel.*

### Deliverables

* All unit and integration tests pass, including those of revision 0.
* User documentation for revision 1 is largely in place and is available online.
* Feedback from beta-testers.

## Phase 5 (Release)

This phase is targeted at creating and maintaining a final release version of revision 1.

### Executed by

* Core maintainers
* Development team (as needed)

### Steps

#### Release candidate 1

1. Apply changes that cannot be delayed until the next minor release, because
    * they fix a bug in the current implementation,
    * they make an important update to the API, i.e., a *major* improvement to the user experience is expected.
1. Apply refinements to documentation as needed.
1. Create release version *1.0.0rc1*.
1. Make minor release announcement.

#### Release candidate 2

1. Apply changes that cannot be delayed until the next minor release, because
    * they fix a *major* bug identified for release candidate 1,
    * they make a very important update to the API, i.e., a *major* detriment to the user experience is expected otherwise.
1. Apply refinements to documentation as needed.
1. Create release version *1.0.0rc2*.
1. Make minor release announcement.

#### Final release

1. Apply fixes to *critical* issues identified for release candidate 2.
1. Apply any changes to the API deemed *critical*, i.e., a *critical* detriment to the user experience is expected otherwise.
1. Create release version *1.0.0*.
1. Make major announcement.

## Phase 6 (Maintenance)

This phase is targeted at maintaining a stable release until the next minor version as well as conducting outreach to publicize the release.

### Executed by

* Maintainers

### Steps

1. Apply for NUMFOCUS affiliation.
1. Conduct online training session.
1. Continually update the documentation based on user feedback received.
1. Create patch releases on regular basis.
