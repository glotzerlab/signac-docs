.. _collections:

============
Collections
============

An instance of :py:class:`~signac.Collection` is a *container* for multiple documents, where a document is an associative array of key-value pairs.
Examples are the job state point, or the job document.

The :py:class:`~signac.Collection` class is used internally to manage and search data space indexes which are generated on-the-fly.
But you can also use such a container explicitly for managing document data.


Creating collections
====================

To create an empty collection, simply call the default constructor:

.. code-block:: python

    from signac import Collection

    collection = Collection()

You can then add documents with the :py:meth:`signac.Collection.insert_one` method.
Alternatively you can pass an iterable of documents as the first argument, such as the return value of the :py:meth:`signac.Project.index` method:

.. code-block:: python

    index_collection = Collection(project.index())

By default, the collection is stored purely in memory.
But you can use the :py:class:`signac.Collection` container also to manage collections **directly on disk**.
For this, simply *open* a file like this:

.. code-block:: python

    with Collection.open('my_collection.txt') as collection:
        pass

A collection file by default is openend in *append plus* mode, that means it is opened for both reading and writing.
The :py:func:`~signac.Collection.open` function accepts all standard file open modes, such as `r` for *read-only*, etc.

Large collections can also be stored in a compressed format using gzip for efficiency.
To use a compressed collection, simply pass in a compression level from 1-9 as a `compresslevel` argument to the :py:class:`signac.Collection` constructor:

.. code-block:: python

    from signac import Collection

    collection = Collection(compresslevel=9)


Searching collections
=====================


To search a collection, use the :py:meth:`signac.Collection.find` method.
As an example, to search all documents where the value ``a`` is equal to 42, execute:

.. code-block:: python

    for doc in collection.find({"a": 42}):
        pass

The :py:meth:`signac.Collection.find` method uses the framework-wide `query` API.

Command Line Interface
======================

To manage and search a collection file directly from the command line, create a python script with the following content:

.. code-block:: python

    from signac import Collection

    with Collection.open("my_collection.txt") as c:
        c.main()

Storing the code above in a file called ``find.py`` and then executing it will allow you to search for all or specific documents within the collection, directly from the command line ``$ python find.py``.

For more information on how to use the command line interface, execute: ``$ python find.py --help``.
