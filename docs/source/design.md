# The *signac* Framework Concepts

## Currently: v0.1-0.9.x

### Definitions

**Job**

A *job* has a *job workspace* and a *job id*.

**Job workspace**

A directory that contains a *signac* metadata file.

**Job id**

A 32-digit hexadecimal number that is a function of the *signac* metadata.

**Project**

A project has a *Project root directory* and manages a *Project workspace*.

**Project root directory**

A file system directory that contains an INI-style *signac* configuration file with the `project` configuration value.

**Project workspace**

A file system directory that contains zero or more *Job workspaces* directories, where each *Job workspace* directory name is equal to the *Job id*.
A *Project workspace* can be any directory within the file system.


### API Examples

```python
>>> import signac

# Get a project handle
>>> project = signac.get_project()

# Get a job handle by metadata
>>> job = project.open_job({'foo: 42'})

# Get a job handle by primary id
>>> job = project.open_job(id='abc123')

>>> print(job.id)
0300c31b9d55c0196b3848d252e46c0f
>>> print(job.sp)
{'foo': 42}

# Migrate a job's state point
>>> job.sp.foo = 48     # Changes state point and directory name.

# Iterate over jobs
>>> for job in project:
...    pass

# Search jobs
>>> selection = project.find_jobs({'foo.$gt': 40})
```

## Proposal: v0.10.0

### Definitions

**State point**

A JSON-encodable key-value mapping, or Null.

**Job**

A directory on the file-system associated with a state point.
If the state point is non-Null, it will be stored in a file signac_statepoint.json within the Job.
**Note: The state point is no longer defined as a unique identifier of the job.**

**Job state point**

The JSON-encoded state point contained by the job.

**Workspace**

A directory that contains a workspace.rc file that defines a `statepoint\_id()` function from arbitrary key-value pairs to 32-hexadecimal strings.
The name of any Job in a workspace must equal the statepoint_id of the job state point; consequently, job names within a workspace must be unique.
A workspace may also contain other arbitrary files, but this usage is strongly discouraged.

**State point ID**

The output of statepoint_id(job) for a state point contained by a job in a given workspace.
The state point ID is workspace-dependent.

**Job state point ID**

The *state point ID* of the job state point.

**Managed job**

A job that is an immediate subdirectory of a workspace.

***signac* configuration file**

An INI-style configuration file named signac.rc or .signacrc.

**Project configuration file**

A signac configuration file with the `project` configuration key defined.
The file should also have the `workspace` key defined, but this key will default to "workspace" if it is empty.

**Project root directory**

A directory that contains a *signac Project configuration file*.

**Project workspace**

A *workspace* that is the value associated with the `workspace` key in the corresponding Project configuration file.

**Project**

An abstract container of a data space composed of jobs. Concretely, a *Project* is defined by its *root directory*, and is therefore associated with a *project workspace*.
This workspace is the only directory that is indexed by the project by default.

**Attached Job**

A *Job* that is a sub-directory of the **current** *Project root directory*.

**Detached Job**

A *Job* that is not a sub-directory of the **current** *Project root directory*.

**Job ID**

For *attached* jobs, the normalized path **relative** to the *current* project workspace directory.
For *detached jobs*, the normalized **absolute** path.
Note that for jobs that are both *managed* and *attached*, the Job ID is equivalent to the *state point ID*.

**Moving a job**

Moving a job's directory to a different location.

**Migrating a job**

Changing the job *state point* and *id* according to some well-defined scheme.
For *managed jobs*, modifying the state point results in automatic migration according to the job workspace's `statepoint\_id()` function.

**Index**

A search index for jobs contained in one or multiple directories that supports finding, grouping, and selection of sets of jobs.

### Python interfaces

The core concepts defined above have the concrete implementations as Python classes.
These are described below.

#### The Job interface

A `signac.Job` enables users to store and retrieve **data and metadata** for a given *file system path*.
The `Job` must be created using the `Job.init` class method, which specifies both path to the job.
This factory function also takes an optional *state point* argument that, if provided, is saved in the JSON-encoded signac_statepoint.json file at the provided path.
The `Job` object then supports storing data within the specified directory.

A `signac.Job` has the following API:
```python
class Job:

    def __init__(self, path):
        """Initialize job for the existing path."""

    @classmethod
    def init(cls, path, statepoint=None, force=False):
        """Initialize job at path with given state point.

        :param path:
            The data directory of the job instance.
        :param statepoint:
            The metadata dictionary associated with the
            directory of the job instance.
        :param force:
            Overwrite any existing state point metadata.
        :returns:
            An instance of `Job`.
        :raises ValueError:
            When the provided value for state point does not
            match the state point value already stored at the
            given path and the force argument is False.
        """

    @property
    def path(self):
        """Returns the job's path relative to the current working directory."""

    @property
    def id(self):
        """Returns the Job ID.

        Depending on whether this job is attached to the current project,
        the ID is either a path relative to the current project's workspaces
        directory or the absolute job path.

        Essentially equivalent to:

            try:
                project = get_project()
                if is_subdir(job.path, project.root_directory()):
                    return os.path.relpath(job.path, str(project.workspace))
                else:
                    raise LookupError
            except LookupError:
                return os.path.abspath(job.path)
        """


    @property
    def statepoint_id(self):
        """Returns the state point ID."""

     def set_permissions(self, mode='0o644'):
         """Set the job's metadata file permissions.

         The default value allows changes to the job's
         state point only by the file owner.

         Equivalent to:

             os.chmod(self._fn_statepoint, mode)
         """

    # Other methods, that are already implemented as part
    # of the legacy signac.contrib.job.Job class.
```


#### The Workspace interface

A `signac.Workspace` enables the automatic generation of paths from *state points*.
By construction, these paths will correspond to *state point IDs*, such that jobs created using these paths will be managed jobs.
Consequently, jobs within any given workspace must be unique up to their state points.

A `signac.Workspace` has the following API:
```python
class Workspace:

    def __init__(self, path):
        """Initialize a Workspace for the given path.

        The constructor should create the workspace.rc configuration file at the provided path."""

    @property
    def path(self):
        """Returns the path relative to the current directory."""

    def __str__(self):
        """Alias for `.path`."""

    def statepoint_id(self, statepoint):
        """Return a relative path for the given state point."""

    def open(self, statepoint):
        """Return a Job at the path defined by statepoint_id(statepoint)."""

    def __call__(self):
        """Alias for `.path` but emits `SignacDeprecationWarning`."""
```


#### The Index interface

A `signac.Index` enables search and selection operations on collections of Jobs.
A `signac.Index` is constructed by crawling the indexed paths and building a collection of documents that link file system paths to Jobs.

A `signac.Index` has the following API:
```python
class Index:

    def __init__(self, * paths, recursive=False, auto_cache=False):
        """Construct index for paths."""

    def build(self, include_documents=False):
        """Build index for paths."""

    def __getitem__(self, id):
        """Return path for the given id.

        :returns:
            A path for the given id.
        :raises KeyError:
            If no match is found for the given id.
        """

    def get(self, id, default=None):
        """Like __getitem__, but returns `default` if no match is found."""

    def lookup(self, id):
        """Return path for the given (abbreviated) id.

        This function will optionally expand the id to generate a match.

        :returns:
            A path for the given id.
        :raises KeyError:
            If no match is found for the given ID, even after expansion.
        :raises LookupError:
            If more than one match was for the given ID.
        """

    def find(self, filter=None, **filter_kwargs):
        """Returns an iterator over paths for the selection.

        This function returns an iterator over all paths that
        match the given filter argument.

        Valid examples:

            find(dict(foo=42))
            find(foo=42)
            find('foo 42')
        """
    def store_cache(self):
        """Store persistent cache for this index in paths."""

    def __call__(self):
        """Return iterator over all entries.

        Primarily needed to preserve backwards compatibility.
        """
```

##### Questions

 * Should `Index` return (iterators over) instances of `Job` instead of paths?
 **Yes, I think so. Jobs are our unambiguous representations of paths anyway.**

#### The Project interface

A `signac.Project` provides an **anchor** on the file system that we can use to abstract away concerns about the data's absolute location.
A `signac.Project` provides a transparent interface to a `signac.Index` on a specific instance of a `signac.Workspace`, namely the *project workspace*.
It allows us to automatically determine a path within the *project workspace* for a given *state point* based on the underlying `Workspace` object, providing a straightforward interface for instantiating new Jobs.
The underlying `Index` object can be used to search and select jobs that are located within the *project workspace*.
Any other jobs may also be searched by explicitly adding them to the project's index (see below for more details).

A `signac.Project` has the following API:

```python
class Project:

    def __init__(self, config):
        """Initialize a Project instance with the given configuration."""

    @property
    def index(self):
        """Return a reference to the project's index instance."""

    @property
    def workspace(self):
        """Return a reference to the project's workspace instance.

        Reset the workspace path on assignment.
        """

    @support_legacy_api
    def find(self, **filter):
        """Build and search the project's workspace index.

        Wrapper for:

            return JobsIterator(self.index.find(**filter)))

        :returns:
            An iterator over instances of `Jobs`.
        """

    find_jobs = find  # legacy API

    def open(self, statepoint=None, id=None):
        """Return instance of job for the given statepoint or id.

        Depending on whether a state point or id is provided,
        this function will either return

            return Job(self.workspace.open(statepoint))

        or

            return self.index.lookup_job(id)

        :returns:
            An instance of `Job` for the given state point or
            matching id.
        :raises KeyError:
            If a job with the given id does not exist.
        :raises LookupError:
            If there is more than one job matching
            an abbreviated id.
        :raises ValueError:
            If both the state point and id argument are provided.
        """

    open_job = open  # legacy API

    def __getitem__(self, id):
        """Return an instance of `Job` for the given id.

        This is equivalent to:

            return Job(self.workspace[id])

        :returns:
            An instance of Job for the given id.
        :raises KeyError:
            If the job directory does not exist.
        """

    def lookup(self, id):
        """Return an instance of Job for the given (abbreviated) id.

        This is equivalent to:

            Job(self.index.lookup(id))

        Note: This function will try to expand a given id,
        to find a match if necessary.

        :returns:
            An instance of Job for the given id.
        :raises KeyError:
            If the job directory does not exist.
        :raises LookupError:
            If there is more than one job matching
            an abbreviated id.
        """

    def is_managed(self, job):
        """Determine whether the job is managed.

        Equivalent to:

            return job.id == self.workspace.open(job.statepoint)

        returns:
            True if job is managed in the workspace, otherwise False.
        """

    # ...
```

##### The Project data space

The project data space consists of the project workspace **as well as all other jobs that are subdirectories of the project root directory**.
That becomes obvious considering that we can obtain **any** job by providing a path relative to the project's workspace directory.
For example, assuming that `~/my_project/` is the project root directory and that there is a job in `~/my_project/data/my_job`, we can obtain a job handle with:
```python
>>> job = project['../data/my_job']
```
However, this job would not be part of the project *find()* result by default, unless we add `~/my_project/data` to the *indexed* directories.
We can still search and select these jobs by either using an explicit index:
```python
>>> index = Index('data')
>>> jobs = index.find('foo.$gt 0')
```
or by adding the `data/` directory to the project's indexed directories:
```python
>>> project.add_index('data/')
```
This equivalent to adding an entry to the project's `indexed` configuration key:
```INI
# signac.rc
project = Project
indexed = data
```

#### User story: Freeze the workspace

One possible advantage of moving *all* jobs from the workspace into a different directory is to essentially *freeze* the workspace, meaning that future state point changes will no longer cause a change to the job's *ID* and *path*.

A simple freeze would be achieved with
```bash
~/my_project $ mv workspace data
```
We then add `data/` to the *indexed* directories with `project.add_index('data/')`.

### Job move and migration

A move operation is achieved by assigning the job a new *path* or a new *ID*.
When a job's state point is modified, a migration may be achieved by also updating the job ID according to some well-defined scheme.
For *managed jobs*, modifying the state point results in an automatic migration according to the workspace's `statepoint_id` function.
(Note: Previously, **all** state point changes were a migration.)

Examples for a simple path assignment:
```python
>>> job.path = '/new/location'  # moves job directory to /new/location
>>> job.path = 'new/location'  # moves job directory to ./new/location
>>> job.path = project.fn('new/location')  # moves job directory to <project-root-directory>/new/location
```

Assigning a new *state point* for a *managed* job will result in a *migration*:
```python
>>> os.chdir('~/my_project')
>>> project = get_project()
>>> job = project.lookup('0300')
>>> print(job.id)
0300c31b9d55c0196b3848d252e46c0f
>>> print(job.path)
workspace/0300c31b9d55c0196b3848d252e46c0f
>>>
... # Assign a new statepoint:
>>> job.sp = dict(foo=43)
>>> print(job.id)
fb5599b2a36a3cc7cd97aeaf6febfe97
>>> print(job.path)
workspace/fb5599b2a36a3cc7cd97aeaf6febfe97
```

A change of the job's *ID* in conjunction with a *state point* change only occurs for *managed* jobs.
For other jobs, changing the *state point* will leave the job ID unchanged.

To further protect the job metadata against accidental changes, it is recommended to set restrictive read/write permissions, for example with:
```python
# Protect workspace against renaming operations by other users:
os.chmod(project.workspace.path, 0o755)

# Protect jobs against state point changes by other users:
for job in project:
    job.set_permissions()
```

Please see below for a pseudo-implementation of the *ID* and *state point* reset operations for the `Job` class.


### Finding jobs with *Project.find_jobs()*

All find-functions will accept queries in three different formats:

1. Dictionary (like before), ex: `find(dict(foo=42))`
2. String (interpreted as simple syntax), ex.: `find('foo 42')`
3. Key-word arguments, ex.: `find(foo=42)`

Furthermore, it is now possible to specify **one** filter that queries both the job *state point* and the job *document* in one expression.
For example, the following expressions are all equivalent:
```python
>>> find('foo 42 doc.bar true')
>>> find('sp.foo 42 doc.bar true')
>>> find({'sp.foo': 42, 'doc.bar': True})
>>> find({'foo': 42}, doc={'bar': True})
>>> find(foo=42, **{'doc.bar': True})
```
The `sp.`-prefix is optional, that means all filter keys that have no prefix are automatically expanded to include this prefix.
The following prefixes are supported: `sp.`, `doc.`, and `id.`

We can consider to support additional prefixes in the future as well, such as `data.`, `isfile.`, etc.

### Summary of API Changes

1. The `signac.Index` class is added that encapsulates the current search and caching functions implemented by the `signac.Project` class API.
1. The `Project.index` function is converted to a property which holds a first-class `Index` object with the *project workspace* as first argument. Calling an `Index` object returns an iterator over all entries, thus preserving backwards-compatibility.
1. The `Project.find_jobs()` function is replaced by `Project.find()` with slightly modified function signature (see above).
1. The `Project.open_job()` function is replaced by `Project.open()`.
1. The `signac.Workspace` class is added that encapsulates the current path generation function implemented by the `signac.Project` and `signac.contrib.job.Job` class API.
1. The `Project.workspace` attribute is converted to a property. Calling the attribute will still be possible but users are warned with a `SignacDeprecationWarning`.
1. It is possible to change the *project workspace directory* by assigning a new value to `Project.workspace`. The user is warned about values which will be illegal in upcoming versions with a `SignacDeprecationWarning`.
1. A revised version of the `signac.contrib.job.Job` class is moved into the root namespace (API shown above), a backwards compatibility layer is maintained at `signac.contrib.job.Job`.
1. Opening a job with `Project.open_job()` returns an instance of `signac.Job` and thus automatically initializes the job. It is not possible to initialize an instance of `signac.Job` for a nonexistent path.

### Additional API Examples

#### Project-based workflows

The project-based workflows rely on the specification of a project root directory.
Standard operations involve the opening (and optional initialization) of *managed* jobs within the project's workspace:
```python
>>> import signac
>>> # Get a project handle
... project = signac.get_project()
>>> print(project.workspace)
'workspace/'
```
Open and potentially initialize a new job by *state point*:
```python
>>> job = project.open_job(dict(foo=42))
>>> print(job.id)
0300c31b9d55c0196b3848d252e46c0f
>>> print(job.sp)
{'foo': 42}
>>> print(job.id)
0300c31b9d55c0196b3848d252e46c0f
>>> print(job.path)
workspace/0300c31b9d55c0196b3848d252e46c0f
>>> print(project.is_managed(job))
True
```
Obtain jobs directly by *ID*:
```python
>>> job = project['0300c31b9d55c0196b3848d252e46c0f']
>>> # or alternatively with abbreviated ID:
... job = project.lookup('0300')  # slightly more expensive
```
Iterate over all or a selection of indexed jobs:
```python
>>> for job in project:
...     print(job.id)
...
0561266e96c880060d71084ddb7e1f21
07774c7f56b9f3782905094e67808674
09e50f33fb3544215e6cef3ac2c3a978
>>> jobs = project.find({'foo.$exists': 0})
>>> print(len(jobs))
3
```

We can **migrate** a *managed* job to a different *state point*:
```python
>>> print(job.sp)
{'foo': 42}
>>> print(job.id)
0300c31b9d55c0196b3848d252e46c0f
>>> print(job.path)
workspace/0300c31b9d55c0196b3848d252e46c0f
>>> # Assign a new state point:
... job.sp.foo = 43
>>> print(job.sp)
{'foo': 43}
>>> print(job.id)
fb5599b2a36a3cc7cd97aeaf6febfe97
>>> print(job.path)
workspace/fb5599b2a36a3cc7cd97aeaf6febfe97
```
#### Non-project based workflows

In addition to interfacing with signac jobs *via* the *Project* interface, we can also initialize/index jobs directly.
This is especially useful when operating on a third-party data space or when combining multiple data spaces.

For example, we can access a job directly, by providing the full path:
```python
>>> # Initialize a job for a specific path and state point:
... job = Job.init('/path/to/job', dict(foo=42))
>>> print(job.id)
'/path/to/job'
>>> print(job.path)
'/path/to/job'
```
In this case both the job *path* and *ID* are absolute and identical, because we are operating outside of a project and therefore **all** jobs are necessarily detached.

### Potential issues

#### Automatic initialization of jobs

One of the potentially most user-notable changes will be presented by the automatic initialization of jobs.
This change has the potential to break user scripts, whenever users rely on delayed initialization,
for example in a scenario like this:
```python
job = project.open_job(my_sp)
job.sp.another_key = 'additional_metadata'
job.init()
```
The prevalence of examples such as the one above is likely low, but almost certainly not zero.
However, in all likelihood, this script would still work correctly, albeit require at least two additional file system operations.

To further mitigate API conflicts, we will ensure that the `Job.init` classmethod can be safely called on an instance of `Job` without side-effects.

### Additional considerations


### Pseudo implementations

#### Job class

**Note: This is outdated, since it still assumes that behavior depends on whether or not a job is *attached*. The implementation should only depend on whether a job is *managed***
Proposed pseudo-implementation of the *ID* and *state point* reset operations of the `Job` class:
```python
class Job:
    # ...
    def _attached(self):
        "Return True if this job is attached to the current project."
        try:
            return is_subdir(self.path, get_project().root_directory())
        except LookupError:
            return False

    @id.setter
    def reset_id(self, new_id):
        "Reset this job's ID to new_id."
        if os.path.isabs(new_id):
            self.path = new_id
            return
        elif not self._attached():
            raise RuntimeError(
                "Job must be attached to current project to be able"
                "to set relative ID!")
        else:
            self.path = os.path.join(str(get_project.workspace), new_id)

    @statepoint.setter
    def reset_statepoint(self, new_statepoint):
        if not self._attached() or is_subdir(os.getcwd(), self.path):
            raise RuntimeError(
                "The current working directory must be a subdirectory "
                "of the job directory for this state point change!")
        elif get_project().is_managed(self):
            self.id = get_project().workspace.open(new_statepoint)
        self._statepoint = new_statepoint
```
