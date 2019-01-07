# The *signac* Framework Concepts

**Authors**

* Carl Simon Adorf <csadorf@umich.edu>
* Vyas Ramasubramani <vramasub@umich.edu>

## Version: 1.0

### Definitions

**Signac configuration file**

An INI-style file named "*signac.rc*" or "*.signacrc*".

**Document**

A JSON-encodable mapping.

**Attributes**

A *document* or null.

**Directory**

A directory on the file system identified by its normalized absolute path and associated with *attributes*.

**Directory path**

The normalized absolute path to the directory on the file system.

**Directory root**

An optional absolute path indicating a root directory for the given directory.

**Directory ID**

The path relative to the directory root.
If no root is set (the default), this is equal to the *directory path*.

**Directory attributes**

*Attributes* associated with a *directory*.
If the attributes are non-null, they are stored in a file called *signac_attrs.json* within the *directory*, conversely the non-existence of said file indicates null *attributes*.

**Directory document**

A unique *document* associated with a *directory*.
Non-empty documents are stored in a file called *signac_document.json* within the *directory*.

**Directory data**

Data encoded and stored in a unique HDF5-file called *signac_data.h5* within the *directory*.

**Directory View**

An immutable view of a *directory*, that means the interface is restricted to functions that do not manipulate the directory metadata or data.

**Attributes ID**

A function that maps *attributes* to a valid directory name.
Illegal return values include: "signac.rc" and ".signacrc".

**Workspace**

A *directory* that contains a *signac configuration file* with the `attrs_id` key that defines a *attributes id* function.
The default function (`MD5v1`) maps to a 32-character long string of hexadecimal characters.
A **valid** *workspace* contains either no directories, directories with only null attributes, or only *directories* with a name equal to the return value of said function.

A *workspace* may also contain other arbitrary files, but this usage pattern is strongly discouraged as it may lead to file and directory name conflicts.

**Managed directory**

A *directory* that is a direct subdirectory of a workspace.

**Directory Index**

A (by default non-recursive) search index for a directory hat supports the selection and grouping of *directories* residing in it.

**Moving a Directory**

Moving a directory on the file system and updating the *directory* instance path value.

**Migrating a directory**

Changing the directory *attributes* and *path* according to some well-defined scheme.

For *managed directories*, modifying the attributes results in automatic migration according to the *attributes id* function of the *workspace* the directory is residing in.

**DirectoryCursor**

An abstract iterator over a specific set of directories.
The cursor allows for iteration and manipulation of a set of directories.

A concrete example for a *DirectoryCursor* is the result of a *Index* selection.

**Project configuration file**

A *signac configuration file* with the `project` configuration key defined.

**Project**

A *Project* is defined by a *project root directory* and has a default workspace ("workspace").

**Project (root) directory**

A directory that contains a *project configuration file*.

**Project workspace**

The *workspace* of a *project*.

**Project index**

A *index* associated with a *project*.

**Job (legacy)**

A *job* is a *directory*.


### Python interfaces

The abstract concepts defined above are implemented by corresponding Python classes.
Their interfaces are defined below.

#### The Path interface

A `signac.Path` implements a [`os.PathLike`](https://docs.python.org/3/library/os.html#os.PathLike) interface and a few other convenience functions.

```python
class Path:

    def __fspath__(self):
        "Return the normalized absolute path."

    def exists(self):
        """Return True if this path exists on the file system.

        Equivalent to:

            return os.path.exists(self)
        """

    def isfile(self):
        """Return True if this path is a file.

        Equivalent to:

            return os.path.isfile(self)
        """

    def isdir(self):
        """Return True if this path is a directory.

        Equivalent to:

            return os.path.isdir(self)
        """

    def join(self, path):
        """Return a path constructed from joining this path and path.

        Equivalent to:

            return type(self)(os.path.join(self, path))
        """

    # Other methods which might be expected here, such as islink() etc.
```

#### The Directory interface

A `signac.Directory` enables users to store and retrieve **data and metadata** for a given *file system path*.
An instance of `Directory` is constructed given a specific file system path.
An alternative factory function `Directory.init` accepts a path and a *attrs* argument and sets the *directory attributes* during construction *if and only if* the current *attributes* are null.
The `Directory` object then supports storing data within the specified directory.

A `signac.Directory` has the following API:
```python
class Directory:

    def __init__(self, path, root=None):
        """Initialize directory for the given path and root.

        The absolute path is constructed by joining root with path.
        The root argument may be omitted in which case path must either
        be an absolute path or root defaults to the current working
        directory.

        The main purpose of the root argument is to allow for a
        shorter presentation of directories. For example, the following
        two directories point to the same absolute path, but are
        not exactly identical since their representation is slightly
        different:

            >>> print(Directory('/path/to/data/my_project'))
            /path/to/data/my_project
            >>> print(Directory('my_project', '/path/to/data/'))
            my_project
        """

    @classmethod
    def init(cls, path, attrs=None, force=False):
        """Initialize directory at path with given attributes.

        :param path:
            The directory path.
        :param attrs:
            The metadata dictionary associated with the
            directory of the directory instance.
        :param force:
            Overwrite the existing non-null attributes.
        :returns:
            An instance of `Directory`.
        :raises ValueError:
            When the current attributes are not null and do
            not match the provided attributes argument unless
            the force argument is True.
        """

    @property
    def path(self):
        """The normalized absolute path of this directory.

        :returns:
            The normalized absolute path of this directory.
        :rtype:
            Path
        """

    __fspath__ = path  # A Directory is also a path-like object.

    @property
    def id(self):
        """Return the path relative to the directory root.

        This function is primarily needed to support the legacy API
        and is essentially equivalent to:

            if self.root:
                return os.path.relpath(self.path, self.root)
            else:
                return self.path
        """

    __str__ = id

    @property
    def attrs(self):
        """Return the attributes associated with this directory.

        The data container for the attributes is mutable. That means
        changes to this interface are directly reflected on the
        file system.

        For example:

            >>> directory.attrs = dict(foo=42)
            >>> print(directory.attrs)
            {"foo": 42}
            >>> directory.attrs.foo += 1
            {"foo": 43}

        To remove the attributes file, set the attributes to None:

            >>> directory.attrs = None
            >>> assert not directory.isfile('signac_attrs.json')
            >>>
        """

    def __getitem__(self, path):
        """Return a directory with a path relative to this directory.

        Equivalent to:

            return Directory(path=path, root=self.path)
        """

    def exists(self):
        """Return True if this directory exists on the file system."""

    def make(self, recursive=True):
        """Attempt to create this directory on the file system.

        This function attempts to create the file system directory
        associated with this instance (recursively by default).

        .. warning::

            Any parent directories created in the process will
            not be deleted upon failure!

        :param recursive:
            When True, also create all parent directories recursively
            if necessary.
        :raises OSError:
            In case that the creation of the directory failed.
        """

    def __enter__(self):
        """Context manager that temporarily switches into this directory.

        For example:

            >>> with directory:
            ...     open('hello.txt').write('world!')
            ...
            >>> print(open(directory.fn('hello.txt')).read()):
            world!
        """

    def fn(self, path):  # legacy
        """Return a path formed from joining this path and path.

        Wrapper for:

            return self.path.join(path)
        """

    def isfile(self, path):  # legacy
        """Return True if this path joined with path points to a file.

        Equivalent to:

            return self.path.join(path).isfile()
        """

    @property
    def index(self):
        """Returns the index associated with this directory.

        Equivalent to:

            return DirectoryIndex(self.path)
        """

    @property
    def workspace(self):
        """Returns the workspace associated with this directory.

        Equivalent to:

            return Workspace(self.path)
        """

    def find(self, **filter):
        """Build and search the directory's indexes.

        Wrapper for:

            return DirectoryIterator(self.index.find(**filter))
        """

    def get(self, attrs=None, **kwargs):
        """Open a directory for the given attributes.

        Essentially equivalent to:

            return Directory(self.workspace.get(attrs, **kwargs))
        """

    # Other methods, that are already implemented as part
    # of the legacy signac.contrib.job.Job class.
```

##### Example API usage:
```python
# Directory class:
>>> import os
>>> print(os.getcwd())
/data
>>> from signac import Directory
>>> project_dir = Directory('my_project')
>>> project_dir
Directory('my_project', root='/data/')
>>> project_dir.path
Path('/data/my_project')
>>> print(project_dir)
'my_project'
>>> project_dir['data']
Directory('data', root='/data/my_project/')
>>> print(project_dir['data'])
data
>>> foo42 = project_dir['data/foo_42']
>>> foo42
Directory('data/foo_42', root='/data/my_project/')
>>> foo42.exists()
False
>>> foo42.make()    # explicit make()
>>> foo42.exists()
True
>>> print(foo42.fn('hello.txt'))
/data/my_project/data/foo_42/hello.txt
>>> foo42.attrs = dict(foo=42)
>>> print(foo42.attrs)
{"foo": 42}
```

#### AttrsID interface

The `signac.AttrsID` interface is a basic *callable* with the
additional `.valid_id()` function which can be used by the *Workspace*
to identify valid ids through simple inspection.
This may lead to significant performance improvements for the determination
of valid workspaces.

```python
class AttrsID:

    @staticmethod
    def __call__(attrs):
        """Return the attrs_id for this attrs."""

    @staticmethod
    def valid_id(id):
        """Return True if the id is recognized as valid.

        This function may be used as *necessary* condition
        for the identification of a valid workspace.

        The default function returns True.
        """
```

#### The Workspace interface

A `signac.Workspace` enables the automatic generation of paths from *attributes*.
By construction, these paths will correspond to *attributes IDs*, such that directories created using these paths will be *managed directories*.
Consequently, all directories within any given workspace must have names corresponding to their respective *attributes*.

A `signac.Workspace` has the following API:
```python
class Workspace:

    def __init__(self, path, attrs_id=None):
        """Initialize an instance of workspace.

        The attrs_id argument must be a callable, but should
        preferably implement the full `AttrsID` interface for
        improved performance.

        :param path:
            The path to the workspace directory.
        :param attrs_id:
            The attrs_id function.
            Defaults to `signac.hashing.MD5v1`.
        """

    def init(self):
        """Initialize this workspace.

        Creates both the directory and the configuration file
        if any of those do not exist yet.

        The configuration file is a '.signacrc' file with the
        `attrs_id` key set to the name of the *attrs_id*
        functor for this workspace.
        """

    @property
    def path(self):
        """Returns the absolute normalized path to this directory."""

    def __str__(self):
        """Alias for `.path`."""

    def attrs_id(self, attrs):
        """Return a relative path for the given attributes."""

    def get(self, attrs, make=True, **kwargs):
        """Return a path defined by the attrs_id function.

        Optionally initializes the workspace if necessary.
        When make is True, essentially equivalent to:

            self.init()
            return Directory.init(
                path=os.path.join(
                    self.path, self.attrs_id(attrs)),
                attrs=attrs).path

        :param attrs:
            The attrs for which we want to open a directory for.
        :param make:
            Create the directory if it does not exist yet.
        :returns:
            Instance of directory for the given attributes.
        :raises CorruptedWorkspaceError:
            If the provided attributes do not match the attributes
            of the directory at the provided path.
        :raises KeyError:
            If the directory corresponding to the attributes does
            not exist and the make argument is False.
        """

    def check(self):
        """Check whether the workspace is valid.

        That means all directories within the workspace path adhere
        to the specified *attrs id* scheme.
        """

    def repair(self):
        """Move all directories within the workspace to the correct paths.

        This function recalculates the path provided by the
        attrs_id function for all directories within the workspace
        and moves them if necessary.
        """

    def __call__(self):
        """Alias for `.path` but emits `SignacDeprecationWarning`."""
```

##### Example API Usage

We can explicitly construct a `Workspace`
```python
>>> Workspace(project_dir['workspace'])
Workspace('/data/my_project/workspace'])
```
Or use the `.workspace` attribute:
```python
>>> project_dir['workspace'].workspace
Workspace('/data/my_project/workspace'])
```
The `Workspace` object then allows us to quickly create directories
for specific *attributes*:
```python
>>> ws = project_dir['workspace'].workspace
>>> ws.attrs_id(dict(foo=42))
0300c31b9d55c0196b3848d252e46c0f
>>> ws.get(foo=42)
Directory('0300c31b9d55c0196b3848d252e46c0f', root='/data/my_project/workspace/')
>>> print(ws.get(foo=42).attrs)
{'foo': 42}
>>> ws.attrs_id.is_valid('0300c31b9d55c0196b3848d252e46c0f')
True
```

#### The Cursor interfaces

All functions that return a selection of some sort should return an instance of cursor that allows the repeated iteration over the selection and length determination.

This is the basic `_Cursor` interface:
```python
class _Cursor:

    def __iter___(self):
        "Return iterator over the underlying selection."

    def __len__(self):
        "Return the length of the underlying selection."
```

The interface below is the description of an abstract interface that a directory cursor should implement.

The interface is similar to the Directory interface itself, but allows operations on iterators.

```python
class AbstractDirectoryCursor:

    @abstractmethod
    def __iter__(self):
        """Iterator over the selection."""

    @abstractmethod
    def __len__(self):
        """Return the length of the underlying selection."""

    def path(self):
        """Iterator over the directory paths.

        Essentially equivalent to:

            for subdir in selection:
                yield subdir.path
        """

    def fn(self, filename):
        """Iterator over filenames for the selection.

        Essentially equivalent to:

            for subdir in selection:
                yield subdir.fn(filename)
        """

    def apply(self, function):
        """Apply function to all directories.

        Returns iterator over the return values.

        Example:

            >>> for foo in selection.apply(lambda d: print(d, d.sp.foo):
            ...     pass    
            ...
            foo_4 4
            foo_8 8
        """

    def apply_parallel(self, function):
        """Apply function to all directories in parallel.

        Like `.apply`, but executes function in parallel.
        """
```
##### Example API Usage

Examples for this interface are shown as part of the API examples for the `DirectoryInterface` class.

#### The DirectoryIndex interface

A `signac.DirectoryIndex` enables selection and grouping operations on directories located within a specific directory.
This is achieved by scanning the indexed path and compiling a collection of documents containing metadata (e.g. the directory attributes).

A `signac.DirectoryIndex` has the following API:
```python
class DirectoryIndex:

    def __init__(self, path, recursive=False, auto_cache=False):
        """Construct index for path."""

    def build(self, include_documents=False):
        """Build index for path."""

    def __getitem__(self, path):
        """Return document for the given path.

        :returns:
            The index document for the given path.
        :raises KeyError:
            If no match is found for the given path.
        """

    def get(self, id, default=None):
        """Like __getitem__, but returns `default` if no match is found."""

    def lookup(self, path):
        """Return document for the given (abbreviated) path.

        This function will optionally expand the id to generate a match.

        :returns:
            A document for the given id.
        :raises KeyError:
            If no match is found for the given ID, even after expansion.
        :raises LookupError:
            If more than one match was for the given ID.
        """

    def find(self, filter=None, **filter_kwargs):
        """Returns an iterator over directories for the selection.

        This function returns an iterator over all paths that
        match the given filter argument.
        """

    def store_cache(self):
        """Store persistent cache for this index in paths."""

    def __call__(self):
        """(legacy) Return iterator over all entries."""
```

##### Example API usage

```python
>>> project_dir.index
DirectoryIndex('/data/my_project')
>>> foo42 = project_dir['data/foo_42']
>>> foo42.attrs = dict(foo=42)
>>> print(len(project_dir['data'].index.find(foo=42)))
1
```
The `Directory.find()` method is wrapper for `Directory.index.find()`, but returns instances of `DirectoryIndexCursor` instead of an iterator over paths.
For demonstration we first create a bunch of directories:
```python
>>> for foo in [4, 8, 15, 16, 23, 42]:
...     project_dir['data/foo_{}'.format(foo)].attrs = dict(foo=foo)
...
```
We can then iterate over all or a selection of directories.
Here, we select all directories where the value for *foo*  is greater than 15:
```python
>>> for subdir in project_dir['data'].find('foo.$gt 15'):
...     subdir
...
Directory('foo_16', root='/data/my_project/data')
Directory('foo_23', root='/data/my_project/data')
Directory('foo_42', root='/data/my_project/data')
>>> for subdir in project_dir['data'].find('foo.$gt 15'):
...     print(subdir)
...
foo_16
foo_23
foo_42
```
We can also apply certain functions directly to the selection, for example to construct a filename:
```python
>>> for fn in project_dir['data'].find('foo.$lte 15').apply(lambda d: d.fn('hello.txt')):
...     pass
...
/data/my_project/data/foo_4/hello.txt
/data/my_project/data/foo_8/hello.txt
/data/my_project/data/foo_15/hello.txt
```
Some functions can be applied directly without passing it to `apply()`, for example, we can achieve the result above with:
```python
>>> for fn in project_dir['data'].find('foo.$lte 15').fn('hello.txt'):
...     print(fn)
...
/data/my_project/data/foo_4/hello.txt
/data/my_project/data/foo_8/hello.txt
/data/my_project/data/foo_15/hello.txt
```

#### The Project interface

A `signac.Project` provides an *anchor* on the file system that we can use to abstract away concerns about the data's absolute location.
A `signac.Project` has a specific *project workspace* that is automatically indexed providing a straightforward interface for instantiating new directories.

A `signac.Project` has the following API:

```python
class Project:

    def __init__(self, path):
        """Initialize a Project instance for the given path.

        :raises ValueError:
            In case that path is not a project root directory.
        """

    @property
    def config(self):
        """Return a reference to the project's configuration."""

    @property
    def workspace(self):
        """Return a reference to the project's workspace instance.

        Resets the workspace path on assignment.

        Essentially equivalent to:

            return Workspace(self.config['workspace_dir'])
        """

    @property
    def index(self):
        """Return a reference to the project's index instance.

        Essentially equivalent to:

            return Index(self.workspace.path)

        **IT SHOULD BE POSSIBLE TO OVERWRITE THIS TO USE SOME DIFFERENT SCHEME! (csa)**
        """

    def __getitem__(self, id):
        """Return a directory for the given id.

        Wrapper for:

            self.workspace.directory[id]
        """
        return

    @support_legacy_api
    def find(self, **filter):
        """Build and search the project's workspace index.

        Wrapper for:

            return DirectorysIterator(self.index.find(**filter)))

        :returns:
            An iterator over instances of `Directorys`.
        """

    find_jobs = find    # legacy API

    @support_legacy_api
    def get(self, attrs=None, **kwargs):
        """Return instance of directory for the given attrs or id.

        Depending on whether attributes or id is provided,
        this function will either return

            return Directory(self.workspace.get(attrs))

        or

            return self.index.lookup_directory(id)

        :returns:
            An instance of `Directory` for the given attributes or
            matching id.
        :raises KeyError:
            If a directory with the given id does not exist.
        :raises LookupError:
            If there is more than one directory matching
            an abbreviated id.
        :raises ValueError:
            If both the attributes and id argument are provided.
        """

    open_job = get  # legacy API

    def __getitem__(self, id):
        """Return an instance of `Directory` for the given id.

        This is equivalent to:

            return Directory(self.workspace[id])

        :returns:
            An instance of Directory for the given id.
        :raises KeyError:
            If the directory does not exist.
        """

    # Example for implementation of legacy functions:
    def fn(self, filename):
        """Return a filename joined with the project root directory.

        Equivalent to:

            return self.directory.join(filename)
        """
    # ...
```

##### Example API usage
```python
>>> project = Directory('my_project').make_project()
>>> project
Project('/data/my_project')
>>> project.directory
Directoy('/data/my_project')
>>> project.workspace
Workspace('/data/my_project/workspace')
>>> project.index
Index('/data/my_project/workspace')
>>> for job in project:
...     job
...
Directory('0300c31b9d55c0196b3848d252e46c0f', root='/data/my_project/workspace/')
>>> print(job)
0300c31b9d55c0196b3848d252e46c0f
>>> job.path
Path('/data/my_project/workspace/0300c31b9d55c0196b3848d252e46c0f')
>>> print(job)
0300c31b9d55c0196b3848d252e46c0f
>>> project.get(foo=42)
Directory('0300c31b9d55c0196b3848d252e46c0f', root='/data/my_project/workspace/')
>>> project.open_job(dict(foo=42))
<string>:1: SignacDeprecationWarning: The Project.open_job() function is deprecated! Please use .get() instead!
Directory('0300c31b9d55c0196b3848d252e46c0f', root='/data/my_project/workspace/')
```

##### The Project data space

The project data space consists of the project workspace **as well as all other directories that are subdirectories of the project root directory**.
That becomes obvious considering that we can obtain **any** directory by providing a path relative to the project's workspace directory.
For example, assuming that `~/my_project/` is the project root directory and that there is a directory in `~/my_project/data/my_directory`, we can obtain a directory handle with:
```python
>>> directory = project['../data/my_directory']
Directory('../data/my_directory', root='/data/my_project/workspace/')
```

### Directory move and migration

A move operation is achieved by assigning the directory a new *path* or a new *ID*.
When a directory's attributes are modified, a migration may be achieved by also updating the directory path according to some well-defined scheme.
For *managed directories*, modifying the attributes results in an automatic migration according to the workspace's `attrs_id` function.
(Note: Previously, **all** attributes changes were a migration.)

Examples for a simple path assignment:
```python
>>> directory.path = '/new/location'  # moves directory directory to /new/location
>>> directory.path = 'new/location'  # moves directory directory to ./new/location
>>> directory.path = project.fn('new/location')  # moves directory directory to <project-root-directory>/new/location
```

Assigning new *attributes* for a *managed* directory will result in a *migration*:
```python
>>> os.chdir('~/my_project')
>>> project = get_project()
>>> directory = project.lookup('0300')
>>> directory
Directory('0300c31b9d55c0196b3848d252e46c0f', root='~/my_project/')
>>> print(directory.id)
0300c31b9d55c0196b3848d252e46c0f
>>> directory.is_managed()
True
>>> # Assign new attrs:
... directory.attrs = dict(foo=43)
>>> print(directory.id)
fb5599b2a36a3cc7cd97aeaf6febfe97
>>> print(directory.path)
~/my_project/workspace/fb5599b2a36a3cc7cd97aeaf6febfe97
```

A change of the directory's *path* in conjunction with *attributes* change only occurs for *managed* directories.
For other directories, changing the *attributes* will leave the directory path unchanged.

To further protect the directory metadata against accidental changes, it is recommended to set restrictive read/write permissions, for example with:
```python
# Protect workspace against renaming operations by other users:
os.chmod(project.workspace.path, 0o755)
```

### Finding directories with *Project.find()*

All find-functions will accept queries in three different formats:

1. Dictionary (like before), ex: `find(dict(foo=42))`
2. String (interpreted as simple syntax), ex.: `find('foo 42')`
3. Key-word arguments, ex.: `find(foo=42)`

Furthermore, it is now possible to specify **one** filter that queries both the directory *attributes* and the directory *document* in one expression.
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

1. The `signac.DirectoryIndex` class is added that encapsulates the current search and caching functions implemented by the `signac.Project` class API.
1. The `Project.index` function is converted to a property which holds a first-class `DirectoryIndex` object with the *project workspace* as first argument. Calling an `DirectoryIndex` object returns an iterator over all entries, thus preserving backwards-compatibility.
1. The `Project.find_jobs()` function is replaced by `Project.find()` with slightly modified function signature (see above).
1. The `Project.open_job()` function is replaced by `Project.get()`.
1. The `signac.Workspace` class is added that encapsulates the current path generation function implemented by the `signac.Project` and `signac.contrib.job.Job` class API.
1. The `Project.workspace` attribute is converted to a property. Calling the attribute will still be possible but users are warned with a `SignacDeprecationWarning`.
1. It is possible to change the *project workspace directory* by assigning a new value to `Project.workspace`. The user is warned about values which will be illegal in upcoming versions with a `SignacDeprecationWarning`.
1. A strongly revised version of the `signac.contrib.job.Job` class is moved into the root namespace under name `signac.Directory `(API shown above). A backwards compatibility layer is maintained.

### Additional API Examples

#### Project-based workflows

The project-based workflows rely on the specification of a project root directory.
Standard operations involve the opening (and optional initialization) of *managed* directories within the project's workspace:
```python
>>> import signac
>>> # Get a project handle
... project = signac.get_project()
>>> print(project.workspace)
'/my_project/workspace/'
```
Open and potentially initialize a new directory by *attributes*:
```python
>>> foo42 = project.get(foo=42)
>>> print(foo42.id)
0300c31b9d55c0196b3848d252e46c0f
>>> print(foo42.attrs)
{'foo': 42}
>>> print(foo42.path)
/my_project/workspace/0300c31b9d55c0196b3848d252e46c0f
>>> print(foo42.is_managed())
True
```
Obtain directories directly by *ID*:
```python
>>> foo42 = project['0300c31b9d55c0196b3848d252e46c0f']
>>> # or alternatively with abbreviated ID:
... foo42 = project.lookup('0300')  # slightly more expensive
```
Iterate over all or a selection of indexed directories:
```python
>>> for directory in project:
...     print(directory)
...
0561266e96c880060d71084ddb7e1f21
07774c7f56b9f3782905094e67808674
09e50f33fb3544215e6cef3ac2c3a978
>>> directories = project.find({'foo.$gt': 0})
>>> directories
IndexCursor('/data/my_project/workspace', {'foo.$gt': 0})
>>> print(len(directories))
3
```

#### Non-project-based workflows

Instead of using `Project` class we can implement a lot of workflows just using the `Directory` class:
```python
>>> my_project = Directory('my_project', '~')
>>> workspace = my_project['workspace']
>>> for foo in [4, 8, 15, 16, 23, 42]:
...     my_project['workspace'].workspace.get(foo=foo)
...
Directory('5beff50c2adf33c7c4aa9ebea3622f46', root='/projects/my_project/workspace/')
Directory('7ba200e881d5aa9a9b27692ab8b02a5e', root='/projects/my_project/workspace/')
Directory('a8cdb2f1357da6e7df3f06e26846efc2', root='/projects/my_project/workspace/')
Directory('80dcf20ae54a2f22939c9182e0705b0b', root='/projects/my_project/workspace/')
Directory('29656cdcda1cbfb88fc82f358defbd34', root='/projects/my_project/workspace/')
Directory('0300c31b9d55c0196b3848d252e46c0f', root='/projects/my_project/workspace/')
>>> for subdir in workspace.find('foo.$lt 16'):
...     print(subdir.path, subdir.attrs())
...
/projects/my_project/workspace/5beff50c2adf33c7c4aa9ebea3622f46 {"foo": 4}
/projects/my_project/workspace/7ba200e881d5aa9a9b27692ab8b02a5e {"foo": 8}
/projects/my_project/workspace/a8cdb2f1357da6e7df3f06e26846efc2 {"foo": 15}
```

#### Multi-Index based workflows

In addition to interfacing with signac directories *via* the *Project* interface, we can also index multiple directories explicitly.
This is especially useful when operating on a third-party data space or when combining multiple data spaces.

For example, we can search multiple directories with a `MultiIndex`:
```python
>>> other_project_index = NameBasedIndex('/data/other_project/', scheme='foo_{foo}')
>>> index = MultiIndex(['/data/my_project/workspace/', other_project_index])
>>> # Initialize a directory for a specific path and attributes:
>>> for subdir in index.find('foo.%exists true'):
...     subdir
...
Directory('0561266e96c880060d71084ddb7e1f21', root='/data/my_project/workspace/')
Directory('07774c7f56b9f3782905094e67808674', root='/data/my_project/workspace/')
Directory('09e50f33fb3544215e6cef3ac2c3a978', root='/data/my_project/workspace/')
Directory('foo_0', root='/data/other_project/')
Directory('foo_1', root='/data/other_project/')
```

### User stories

#### Ideal-gas example (basic)

##### Project-based API
Generation:
```python
from signac import init_project

project = init_project('ideal-gas-project')

for p in range(1, 11):
    sp = {'p': p, 'kT': 1.0, 'N': 1000}
    with project.get(sp) as job:
        volume = job.attrs.N * job.attrs.kT / job.attrs.p
        with open('volume.txt') as file:
            file.write(str(volume) + '\n')
```
Presentation:
```python
from signac import get_project

project = get_project('ideal-gas-project')
for job in project.find({'p.$lt 5'}):
    print(job.attrs())
```
##### Non-project based API

Generation:
```python
# compute.py
from signac import Directory

project = Directory('ideal-gas-project')
for p in range(1, 11):
    sp = {'p': p, 'kT': 1.0, 'N': 1000}
    with project['workspace'].get(sp) as subdir:
        volume = subdir.attrs.N * subdir.attrs.kT / subdir.attrs.p
        with open('V.txt', 'w') as file:
            file.write(str(volume) + '\n')
```
Presentation:
```python
from signac import Directory
import signac

project = Directory('ideal-gas-project')
for subdir in project['workspace'].find({'p.$lt 5'}):
    print(subdir.attrs())
```

#### Ideal-gas example (operation-based)

##### Directory-based API

```python
from signac import Directory

def compute_volume(job):
    volume = job.attrs.N * job.attrs.kT / job.attrs.p
    with open(job.fn('volume.txt'), 'w') as file:
        file.write(str(volume) + '\n')

project = Directory('ideal-gas-project')
for p in range(1, 11):
    project['workspace'].get(N=1000, kT=1.0, p=p)

project['workspace'].find().apply(compute_volume)
```

## Version: 0.x

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
