.. _jobs:

====
Jobs
====

.. currentmodule:: signac.contrib.job

Overview
========

A *job* is a directory on the file system, which is part of a *project workspace*.
That directory is called the *job workspace* and contains **all data** associated with that particular job.
Every job has a unique address called the *state point*.

There are two ways to associated metadata with your job:

1. As part of the :attr:`Job.statepoint` (aliased by :attr:`Job.sp`).
2. As part of the :attr:`Job.document` (aliased by :attr:`Job.doc`).

Both containers have the exact same (dict-like) interface and capabilities, both are indexed (that means searchable), but only the former represents the unique address of the job.
In other words, all data associated with a particular job should be a direct or indirect function of the *state point*.

.. important::

    Every parameter that, when changed, would invalidate the job's data, should be part of the *state point*; all others should not.

However, you only have to add those parameters that are **actually changed** (or anticipated to be changed) to the *state point*.
It is perfectly acceptable to hard-code parameters up until the point where you **actually change them**, at which point you would add them to the *state point* :ref:`retroactively <add-sp-keys>`.

You can, but do not have to use the :class:`Job` interface to associate data with a job.
Any file --with a name and format of your choosing-- that is stored within the job's workspace directory is considered *data associated with the job*.

However, if you do choose to interact with the data through the :class:`Job` interface, there are four main ways of doing so:

1. You temporarily change the working directory to the job's workspace directory by using the job as a context manager (``with job:``).
2. You use the :meth:`Job.fn` function to construct file paths, where ``job.fn('data.txt')`` is equivalent to ``os.path.join(job.workspace(), 'data.txt')``.
3. You store (small) JSON-serializable data in the :attr:`Job.document`.
4. You store (small or large) numerical array-like data in the :attr:`Job.data` container.

All three data containers :attr:`Job.statepoint`, :attr:`Job.document`, and :attr:`Job.data` provide a highly similar dict-like interface, which is described in more detail in the following sections.

.. _project-job-statepoints:

The Job State Point
===================

A *state point* is a simple mapping of key-value pairs containing metadata describing the job.
The state point is then used to compute a hash value, called the *job id*, which serves as the unique id for the job.
The **signac** framework keeps track of all data and metadata by associating each job with a *workspace directory*, which is just a subdirectory of the project workspace.
This subdirectory is named by the *job id*, therefore guaranteeing a unique file system path for each *job* within the project's *workspace* directory.

.. note::

    Because **signac** assumes that the state point is a unique identifier, multiple jobs cannot share the same state point.
    A typical remedy for scenarios where, *e.g.*, multiple replicas are required, is to append the replica number to the state point to generate a unique state point.

Both the state point and the job id are equivalent addresses for jobs in the data space.
To access or modify a data point, obtain an instance of :py:class:`Job` by passing the associated metadata as a mapping of key-value pairs (for example, as an instance of :py:class:`dict`) into the :py:meth:`~signac.Project.open_job` method.

.. code-block:: python

    # Define a state point:
    >>> statepoint = {'a': 0}
    # Get the associated job:
    >>> job = project.open_job(statepoint)
    >>> print(job.get_id())
    9bfd29df07674bc4aa960cf661b5acd2


In general an instance of :py:class:`Job` only gives you a handle to a python object.
To create the underlying workspace directory and thus make the job part of the data space, you must *initialize* it.
You can initialize a job **explicitly**, by calling the :py:meth:`Job.init` method, or **implicitly**, by either accessing the job's :ref:`job document <project-job-document>` or by switching into the job's workspace directory.

.. code-block:: python

    >>> job = project.open_job({'a': 2})
    # Job does not exist yet
    >>> job in project
    False
    >>> job.init()
    # Job now exists
    >>> job in project
    True

Once a job has been initialized, it may also be *opened by id* as follows (initialization is required because prior to initialization the job id has not yet been calculated):

.. code-block:: python

    >>> job.init()
    >>> job2 = project.open_job(id=job.get_id())
    >>> job == job2
    True

Whether a job is opened by state point or job id, an instance of :py:class:`Job` can always be used to retrieve the associated *state point*, the *job id*, and the *workspace* directory with the :py:attr:`Job.statepoint`, :py:meth:`Job.get_id`, and :py:meth:`Job.workspace` methods, respectively:

.. code-block:: python

    >>> print(job.statepoint())
    {'a': 0}
    >>> print(job.get_id())
    9bfd29df07674bc4aa960cf661b5acd2
    >>> print(job.workspace())
    '/home/johndoe/my_project/workspace/9bfd29df07674bc4aa960cf661b5acd2'

Evidently, the job's workspace directory is a subdirectory of the project's workspace and is named by the job's id.
We can use the :py:meth:`Job.fn` function to prepend the workspace path to a file name; ``job.fn(filename)`` is equivalent to ``os.path.join(job.workspace(), filename)``.
This function makes it easy to create or open files which are associated with the job:

.. code-block:: python

    >>> print(job.fn('newfile.txt'))
    '/home/johndoe/my_project/workspace/9bfd29df07674bc4aa960cf661b5acd2/newfile.txt'

For convenience, the *state point* may also be accessed via the :py:attr:`Job.statepoint` or :py:attr:`Job.sp` attributes, e.g., the value for ``a`` can be printed using either ``print(job.sp.a)`` or ``print(job.statepoint.a)``.
This also works for **nested** *state points*: ``print(job.sp.b.c)``!

.. _project-job-statepoint-modify:

Modifying the State Point
-------------------------

As just mentioned, the state point of a job can be changed after initialization.
A typical example where this may be necessary, is to add previously not needed state point keys.
Modifying a state point entails modifying the job id which means that the state point file needs to be rewritten and the job's workspace directory is renamed, both of which are computationally cheap operations.
The user is nevertheless advised **to take great care when modifying a job's state point** since errors may render the data space **inconsistent**.

There are three main options for modifying a job's state point:

    1. Directly via the job's :py:attr:`Job.statepoint` and :py:attr:`Job.sp` attributes,
    2. via the job's :py:meth:`Job.update_statepoint` method, and
    3. via the job's :py:meth:`Job.reset_statepoint` method.

The :py:meth:`Job.update_statepoint` method provides safeguards against accidental overwriting of existing *state point* values, while :py:meth:`Job.reset_statepoint` will simply reset the whole *state point* without further questions.
The :py:attr:`Job.statepoint` and :py:attr:`Job.sp` attributes provide the greatest flexibility, but similar to :py:meth:`Job.reset_statepoint` they provide no additional protection.

.. important::

    Regardless of method, **signac** will always raise a :py:class:`~signac.errors.DestinationExistsError` if a *state point* modification would result in the overwriting of an existing job.


The following examples demonstrate how to **add**, **rename** and **delete** *state point* keys using the :py:attr:`Job.sp` attribute:

.. _add-sp-keys:

To **add a new key** ``b`` to all existing *state points* that do not currently contain this key, execute:

.. code-block:: python

    for job in project:
        job.sp.setdefault('b', 0)

**Renaming** a state point key from ``b`` to ``c``:

.. code-block:: python

    for job in project:
        assert 'c' not in job.sp
        job.sp.c = job.statepoint.pop('b')

To **remove** a state point key ``c``:

.. code-block:: python

    for job in project:
        if 'c' in job.sp:
            del job.sp['c']

You can modify **nested** *state points* in-place, but you will need to use dictionaries to add new nested keys, e.g.:

.. code-block:: python

    >>> job.statepoint()
    {'a': 0}
    >>> job.sp.b.c = 0  # <-- will raise an AttributeError!!

    # Instead:
    >>> job.sp.b = {'c': 0}

    # Now you can modify in-place:
    >>> job.sp.b.c = 1

.. warning::

    The statepoint object behaves like a dictionary in most cases,
    but because it persists changes to the filesystem, making a copy
    requires explicitly converting it to a dict. If you need a
    modifiable copy that will not modify the underlying JSON file,
    you can access a dict copy of the statepoint by calling it, e.g.
    ``sp_dict = job.statepoint()`` instead of ``sp = job.statepoint``.
    For more information, see :class:`~signac.JSONDict`.


.. _project-job-document:

The Job Document
================

In addition to the state point, additional metadata can be associated with your job in the form of simple key-value pairs using the job :py:attr:`~Job.document`.
This *job document* is automatically stored in the job's workspace directory in `JSON`_ format.
You can access it via the :py:attr:`Job.document` or the :py:attr:`Job.doc` attribute.

.. _`JSON`: https://en.wikipedia.org/wiki/JSON

.. code-block:: python

    >>> job = project.open_job(statepoint)
    >>> job.doc['hello'] = 'world'
    # or equivalently
    >>> job.doc.hello = 'world'

Just like the job *state point*, individual keys may be accessed either as attributes or through a functional interface, *e.g.*.
The following examples are all equivalent:

.. code-block:: python

    >>> print(job.document().get('hello'))
    world
    >>> print(job.document.hello)
    world
    >>> print(job.doc.hello)
    world

.. tip::

     Use the :py:meth:`Job.document.get` method to return ``None`` or another specified default value for missing values. This works exactly like with Python's built-in dictionaries (see :py:meth:`dict.get`).

Use cases for the **job document** include, but are not limited to:

  1) **storage** of *lightweight* data,
  2) Tracking of **runtime information**
  3) **labeling** of jobs, e.g. to identify error states.

.. tip::

    Large arrays of numerical data are often not conducive to store in the :py:attr:`Job.document`. Text-based formats like JSON can be slower and less precise for floating-point numbers. For this kind of data, consider using the :py:attr:`Job.data` container.

.. _project-job-data:

Job Data Storage
================
Job associated data may be stored through :py:attr:`Job.data` or :py:attr:`Job.stores`.
This :py:attr:`Job.data` container uses a file in `HDF5 <https://portal.hdfgroup.org/display/HDF5/HDF5>`_ format to store array-like or dictionary-like information.
Like the :py:attr:`Job.document`, this information can be accessed using key-value pairs.
Unlike the :py:attr:`Job.document`, :attr:`Job.data` is not searchable.
This section will focus on examples and usage of :py:attr:`Job.data`.

Data written with :py:attr:`Job.data` is stored in a file named ``signac_data.h5`` in the associated job folder.
Data written with :py:attr:`Job.stores['key_name']` is stored in a file named ``key_name.h5``.
For cases where job-associated data may be accessed from multiple sources at the same time or other instances where multiple files may be preferred to one large file, :py:attr:`Job.stores` should be used instead of :py:attr:`Job.data`.
Further discussion of :py:attr:`Job.stores` is provided in the following section, Job Stores.

Reading and Writing data
------------------------

An example of storing data:

.. code-block:: python

    >>> import numpy as np
    >>> job = project.open_job(statepoint)
    >>> job.data['x'] = np.ones([10, 3, 4])


Just like the job *state point* and *document*, individual keys may be accessed either as attributes or through a functional interface, *e.g.*.

To access data as an attribute:

.. code-block:: python

    >>> with job.data:
    ...     x = job.data.x[:]

To access data as a key:

.. code-block:: python

    >>> with job.data:
    ...     x = job.data['x'][:]

Through a functional interface:

.. code-block:: python
    
    >>> with job.data:
    ...     x = job.data.get('x')[:]

.. tip::

     Use the :py:meth:`Job.data.get` method to return ``None`` or another specified default value for missing values. This works exactly like with python's built-in dictionaries (see :py:meth:`dict.get`). 
    
Accessing arrays
----------------

All values stored in :attr:`job.data` are returned as copies, except for arrays, which are accessed *by reference* and not automatically copied into memory.
That is important to enable the storage of massive arrays that do not necessarily fit into memory.

For fast and efficient data access, NumPy slicing syntax may be used to access data. 
Here are a few examples for accessing a three-dimensional array with outputs omitted:
   
.. code-block:: python
    
    >>> with job.data:
    ...     job.data.x[0, 0, 0]
    ...     job.data.x[1:3, 0, :]
    ...     job.data.x[:, 1, 3]
    
To load entire arrays to memory, NumPy slicing syntax may be used:
 
.. code-block:: python

    >>> with job.data:
    ...     x = job.data.x[:]

NumPy slicing (ie. the ``[:]`` operator) may be used to load array-like and text data.
It cannot be used to load scalar values.
Instead, the explicit memory copy operator ``[()]`` may be used instead of NumPy slicing to load entire arrays or scalars to memory:

.. code-block:: python

    >> with job.data:
    ..      x = job.data.x[()]

A caveat of the explicit memory copy operator ``[()]`` is that it cannot be used to load strings.
Generally, the :py:attr:`job.data` container is intended for large numerical or text data while information which needs to be searchable and scalars should be stored in the :ref:`job document <project-job-document>`.


Data organization
-----------------

The `HDF5`_ format used by :attr:`job.data` allows for hierarchical organization of data. 
Data may be stored in folder-like *groups*:

.. code-block:: python
    
    >>> job.data['group/subgroup_1'] = np.ones([10, 3, 2])
    >>> job.data['group/subgroup_2'] = np.ones([10, 1, 2])

Data may be accessed as attributes, keys, or through a functional interface.
The following examples are all equivalent:

.. code-block:: python
    
    >>> with job.data:
    ...     job.data.group.subgroup_1[:]
    ...     job.data['group/subgroup_1'][:]
    ...     job.data.get('group/subgroup_1')[:]
    
Accessing keys
--------------

*Groups* and keys in :attr:`job.data` behave similarly to dictionaries. 
To view the keys in a group:

.. code-block:: python
    
    >>> print(list(job.data.keys()))
    ['x', 'group']
    >>> print(list(job.data.group.keys()))
    ['subgroup_1', 'subgroup_2']

To check if keys exist in a group:

.. code-block:: python
    
    >>> 'subgroup_1' in job.data
    False
    >>> 'subgroup_1' in job.data.group
    True
 
To iterate through keys in a group (outputs omitted):

.. code-block:: python

    >>> group = job.data.group
    >>> for key in group:
    ...     group[key][:]


File handling
-------------

The underlying HDF5 file is openend and flushed after each read- and write-operation.
You can keep the file explicitily open using a context manager.
The file is only opened and flushed once in the following example:

.. code-block:: python

    >>> with job.data:
    ...     job.data['hello'] = 'world'
    ...     print(job.data.x)
    ...

The default open-mode is append ("a"), but you can override the open-mode, by using the :meth:`signac.H5Store.open` function explicitly.
For example, to open the store in read-only mode, you would write:

.. code-block:: python

    >>> with job.data.open(mode='r'):
    ...     print(job.data.x)

Explicitly opening the underlying file by either using the context manager or the ``open()`` function is required when reading and writing arrays, such as ``numpy.arrays``.
Please see the next section for details on accessing arrays.

.. warning::

    It is strongly advised that operations on :py:attr:`Job.data` are not performed in parallel, to avoid data corruption.

Low-level API
-------------

The :class:`~signac.H5Store` class that provides the interface for :attr:`Job.data` implements a dict-like interface to provide a homogeneous interface between :attr:`Job.statepoint`, :attr:`Job.document`, and :attr:`Job.data`.
However, in some cases it may be desirable to use more *advanced* functions provided by the ``h5py`` library itself, which we consider *low-level* API in this context.

The low-level API is exposed as the :attr:`~signac.H5Store.file` property, which is accessible whenever the store is open.
For example, this is how we could use that to explicitly create an array:

.. code-block:: python

    >>> with job.data:
    ...     dset = job.data.file.create_dataset("X", (64, 32), dtype='f4')

.. note::

    The file must be open to access the :attr:`~signac.H5Store.file` property!

Please see the h5py_ documentation for more information on how to interact with ``h5py.File`` objects.

.. _`h5py`: http://docs.h5py.org/en/latest/


Job Stores
==========

As mentioned before, the :attr:`Job.data` property represents an instance of :class:`~signac.H5Store`, specifically one that operates on a file called ``signac_data.h5`` in the job workspace.
However, there are some reasons why one would want to operate on multiple different HDF5_ files instead of only one.

 1. While the HDF5-format is generally mutable, it is fundamentally designed to be used as an immutable data container.
    It is therefore advantageous to write large arrays to a new file instead of modifying an existing file many times.
 2. It easier to synchronize multiple files instead of just one.
 3. Multiple operations executed in parallel can operate on different files circumventing file locking issues.

The :attr:`Job.stores` property provides a dict-like interface to access *multiple different* HDF5 files within the job workspace directory.
In fact, the :attr:`Job.data` container is essentially just an alias for ``job.stores.signac_data``.

For example, to store an array `X` within a file called ``my_data.h5``, one could use the following approach:

.. code-block:: python

    with job.stores.my_data as data:
        data['X'] = X


The :attr:`Job.stores` attribute is an instance of :class:`signac.H5StoreManager` and implements a dict-like interface.
