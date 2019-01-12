# Development Plan for Revision 1.0

**Authors**

* Carl Simon Adorf (csadorf@umich.edu)

## About

This document describes the development plan for the implementation of design specifications for signac (core) **revision 1** and is maintained by the signac core maintainers.
The development plan will be continually updated to account for changes and refinements during the execution of this process.

**Targeted audience**

* Core maintainers

## Phase 1 (Planning)

The initial phase is targeted at deciding on the general concept and API for **revision 1** as well as setting up a plan for assembling a developer team and obtaining general buy-in by expert users.

### Executed by

* Core maintainers

### Steps

1. Refine design specifications until consensus among maintainers is reached.
1. Determine developer team candidate pool and communication channels for outreach.
1. Create a landing page for new developers (https://development.signac.io/)
 1. Current status
 1. Development blog
 1. Links
1. Setup the toolchain for
 1. Communication
 1. Document management
 1. Source code management
 1. Issue tracking
 1. Project task tracking


### Deliverables

* A maintainer-approved revision of the design specifications.
* A team candidate pool and a list of communication channels.

## Phase 2 (Pre-Alpha)

This phase is targeted at creating a minimal prototype which can be used for demonstration purposes, assembling an initial developer team, and setting up the development workflow.

### Executed by

* Core maintainers
* Core developers

### Steps

1. **KICK-OFF**: Prepare prototype implementation
 1. Create branch *revision-1* based off *master*.
 1. Implement a single minimal module that demonstrates code and documentation style for developers approved by maintainers.
 1. Implement a minimal test module that demonstrates use of the testing framework.
 1. Create initial set of development guidelines.
1. Implement a minimal skeleton prototype that is demonstration-ready (**v1.0.dev0**).
1. Revise design specifications based on feedback received for prototype.
1. Implement a minimal prototype that demonstrates paths towards backwards-compatibility (**v1.0.dev1**).
1. Reach out to candidate developers and users to aggregate a team of people who are interested in contributing by:
 * writing code
 * writing documentation
 * testing code
 * providing feedback
1. Consider the implementation of an advisory board constituted by experts in the field who advise the core development team on
 * the design specification,
 * the planning and execution of development,
 * publication and outreach activities.
1. Determine
 * development platform
 * communication channels
 * tentative deadlines
1. Create
 * initial work packages
 * development guidelines (https://development.signac.io)
 * conceptual outline of the overall revised user documentation

*Steps xx are executed in parallel.*

### Deliverables

 * Minimal Prototype implementation that allows execution of the core API examples shown in the design specifications.
 * Team member list with roles for
  * developers
  * alpha-testers
  * beta-testers
  * advisers
 * A decision on the development platform (Bitbucket vs. GitHub vs. GitLab etc.)
 * Work packages and development guidelines for tentative developer team
 * Basic outline of the user documentation.
 * Feedback from users and developers on minimal prototype

## Phase 3 (Alpha)

This phase is targeted at creating an alpha-version that is fully compliant with the specifications, and has a partially complete automated testing framework.

### Executed by

* Core maintainers
* Core developers
* Developers
* Alpha-testers

This phase is targeted at polishing the design specifications and revised API, developing  user documentation, and developing prototypes to obtain backwards compatibility.

### Steps

1. Implement alpha-version that is fully compliant with the revised API and has a test coverage of at least 50%.
1. Create a deprecation schedule.
1. Draft a revised version of the overall user documentation.
1. Create tagged revision *v1.0.0alpha*.
1. Obtain feedback from alpha-testers.

*Steps xx are executed in parallel.*

### Deliverables

* Full implementation of revised API.
* Test coverage of at least 50% of all unit and integration tests.
* Deprecation schedule
* Feedback from alpha-testers.
* Revised design specifications.

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

    *Full compatibility may not be possible to achieve in some cases. The core maintainers will decide which tests can be changed or removed.*

1. Complete and refine the user documentation on revised API.
1. Create tagged revision *v1.0.0beta*.
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
