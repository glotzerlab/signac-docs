.. _query:

=========
Query API
=========

As briefly described in :ref:`project-job-finding`, the :py:meth:`~signac.Project.find_jobs()` method provides much more powerful search functionality beyond simple selection of jobs with specific :term:`state points <state point>`.
One of the key features of **signac** is the possibility to search the :term:`project` workspace to select desired subsets as needed.

It is possible to use search expressions directly on the command line, for example in combination with the ``$ signac find`` command.
In this case, filter arguments are expected to be provided as valid JSON expressions.
Notably, JSON writes booleans like ``true`` and ``false`` as opposed to Python's ``True`` and ``False``.


Query Namespaces
================

Filter keys are *namespaced* by the type of the key.
This means that any filter can be used to simultaneously search for keys in both the job state point and the job document.
Namespaces are identified by prefixing filter keys with the appropriate prefixes.
Currently, the following prefixes are recognized:

  * **sp**: job :term:`state point`
  * **doc**: :term:`job document`

For example, to select all jobs whose state point key *a* has the value "foo" and document key *b* has the value "bar", you would use:

.. code-block:: python

    project.find_jobs({"sp.a": "foo", "doc.b": "bar"})

The default prefix is **sp**, so any filter key that does not have a recognized prefix will be matched against job state points.
This means that the following query is equivalent to the one above:

.. code-block:: python

    project.find_jobs({"a": "foo", "doc.b": "bar"})


Basic Expressions
=================

Filter arguments are a mapping of expressions, where a single expression consists of a key-value pair.
All selected documents will match these expressions.


The simplest expression is an *exact match*.
For example, in order to select all jobs whose state point key *a* has the value 42, you would use the following expression: ``{"a": 42}`` as follows:

.. code-block:: python

    project.find_jobs({"a": 42})

.. code-block:: bash

    signac find '{"a": 42}'

Select All
----------

If you want to select the complete data set, don't provide any filter argument at all.
The default argument of ``None`` or an empty expression ``{}`` will select all jobs or documents.
As was previously demonstrated, iterating over all jobs in a project can be accomplished directly.

.. code-block:: python

    for job in project:
        pass

On the command line, ``signac find`` without an arguments will return a list of all jobs.

.. code-block:: bash

    signac find

.. _simple-selection:

Simple Selection
----------------

To select documents by one or more specific key-value pairs, provide these directly as filter arguments.
For example, assuming that we have a list of documents with values *N*, *kT*, and *p*, as such:

.. code-block:: bash

    1: {"N": 1000, "kT": 1.0, "p": 1}
    2: {"N": 1000, "kT": 1.2, "p": 2}
    3: {"N": 1000, "kT": 1.3, "p": 3}
    ...

We can select the 2nd document with ``{'p': 2}``, but also ``{'N': 1000, 'p': 2}`` or any other matching combination.

.. _nested-keys:

Nested Keys
-----------

To match **nested** keys, avoid nesting the filter arguments, but instead use the ``.``-operator.
For example, if the documents shown in the example above were all nested like this:

.. code-block:: bash

    1: {"statepoint": {"N": 1000, "kT": 1.0, "p": 1}}
    2: {"statepoint": {"N": 1000, "kT": 1.2, "p": 2}}
    3: {"statepoint": {"N": 1000, "kT": 1.3, "p": 3}}
    ...

Then we would use ``{'statepoint.p': 2}`` instead of ``{'statepoint': {'p': 2}}`` as filter argument.
This is not only easier to read, but also increases compatibility with MongoDB database systems.

Operator Expressions
====================

In addition to simple exact value matching, **signac** also provides **operator-expressions** to execute more complicated search queries.

.. _arithmetic-operators:

Arithmetic Expressions
----------------------

If we wanted to match all documents where *p is greater than 2*, we would use the following filter argument:

.. code-block:: python

    project.find_jobs({"p": {"$gt": 2}})

.. code-block:: bash

    signac find '{"p": {"$gt": 2}}'

Note that we have replaced the value for p with the expression ``{'$gt': 2}`` to select all jobs with p values greater than 2.
Here is a complete list of all available **arithmetic operators**:

  * ``$eq``: equal to
  * ``$ne``: not equal to
  * ``$gt``: greater than
  * ``$gte``: greater or equal to
  * ``$lt``: less than
  * ``$lte``: less than or equal to

.. _near-operator:

Near Operator
-------------
The ``$near`` operator is used to find jobs with state point parameters that are near a value, where floating point precision may make it difficult to match the exact value.
The behavior of ``$near`` matches that of Python's `math.isclose <https://docs.python.org/3/library/math.html#math.isclose>`_ function.
The "reference" value and tolerances are passed in as a list in the order ``[reference, [relative_tolerance, [absolute_tolerance]]]``, where the inner ``[]``\s denote optional values.
Note that default values are ``relative_tolerance = 1e-09`` and ``absolute_tolerance = 0``.

.. code-block:: bash

    signac find theta.\$near 0.6  # easier than typing 0.600000001
    signac find '{"p.$near": [100, 0.05]}'  # p within 5% of 100
    signac find '{"p.$near": [100, 0.05, 2]}'  # abs(p-100)/max(p, 100) < 0.05 or abs(p-100) < 2

.. _logical-operators:

Logical Operators
-----------------

There are three supported logical operators: ``$and``, ``$or``, and ``$not``.
The first two are unique in that they involve combinations of other query operators.
To query with one of these two logical expression, we construct a mapping with the logical operator as the key and a list of expressions as the value.
As usual, the ``$and`` operator matches documents where all the expressions are true, while the ``$or`` expression matches if documents satisfy any of the provided expressions.
For example, to find all documents where *p is greater than 2* **or** *kT=1.0*, we could use the following:

.. code-block:: python

    project.find_jobs({"$or": [{"p": {"$gt": 2}}, {"kT": 1.0}]})

.. code-block:: bash

    signac find '{"$or": [{"p": {"$gt": 2}}, {"kT": 1.0}]}'


Logical expressions may be nested but cannot be the *value* of a key-value expression.

For the ``$not`` operator, we again construct a mapping with the operator as the key, but the value is a single expression rather than a list of expressions.
For example, to find all jobs where a parameter *a* is not close to zero, we could use the following:

.. code-block:: python

    project.find_jobs({"$not": {"a": {"$near": 0}}})

.. _exists-operator:

Exists Operator
---------------

.. warning::

   Boolean expressions are written differently on the command line because the command line takes JSON formatting.

If you want to check for the existence of a specific key but do not care about its actual value, use the ``$exists``-operator.
For example, this expression will return all documents that *have a key p* regardless of its value.
Likewise, using ``False`` as argument would return all documents that have no key with the given name.

.. code-block:: python

    project.find_jobs({"p": {"$exists": True}})

On the command line, this expression must be written in JSON encapsulated in single quotes:

.. code-block:: bash

    signac find '{"p": {"$exists": true}}'

.. _array-operator:

Array Operator
--------------

This operator may be used to determine whether specific keys have values, that are **in** (``$in``), or **not in** (``$nin``) a given array, e.g.:

.. code-block:: python

    project.find_jobs({"p": {"$in": [1, 2, 3]}})

.. code-block:: bash

    signac find '{"p": {"$in": [1, 2, 3]}}'

This would return all documents where the value for *p* is either 1, 2, or 3.
The usage of ``$nin`` is analogous and will return all documents where the value is *not in* the given array.

.. _regex-operator:

Regular Expression Operator
---------------------------

This operator may be used to search for documents where the value of type ``str`` matches a given *regular expression*.
For example, to match all documents where the value for *protocol* contains the string "assembly", we could use:

.. code-block:: python

    project.find_jobs({"protocol": {"$regex": "assembly"}})

.. code-block:: bash

    signac find '{"protocal": {"$regex": "assembly"}}'

This operator internally applies the :py:func:`re.search` function and will never match if the value is not of type ``str``.

To negate a regular expression use a `negative lookaround`_, *e.g.*, to match all state points where the protocol does **not** contain the word "assembly",
you would use:

.. code-block:: python

   project.find_jobs({"protocol": {"$regex": r"^(?!.*assembly).*$"}})

.. _negative lookaround: https://www.regular-expressions.info/lookaround.html

.. tip::

    Use the `Regex101 <https://regex101.com/>`_ app to develop and test your regular expressions.

.. _type-operator:

Type Operator
-------------

This operator may be used to search for documents where the value is of a specific type.
For example, to match all documents, where the value of the key *N* is of integer-type, we would use:

.. code-block:: python

    project.find_jobs({"N": {"$type": "int"}})

Other supported types include *float*, *str*, *bool*, *list*, and *null*.

.. code-block:: bash

    signac find '{"N": {"$type": "int"}}'

.. _where-operator:

Where Operator
--------------

This operator allows us to apply a *custom function* to each value and select based on its return value.
For example, instead of using the regex-operator, as shown above, we could write the following expression:

.. code-block:: python

    project.find_jobs({"protocol": {"$where": 'lambda x: "assembly" in x'}})

.. code-block:: bash

    signac find '{"protocol": {"$where": "lambda x: \"assembly\" in x"}}'

.. _simplified-filter:

Simplified Syntax on the Command Line
=====================================

For simple filters, you can use a simplified syntax instead of writing JSON.
For example, instead of ``signac find '{"p": 2}'``, you can type ``signac find p 2``.

A simplified expression consists of key-value pairs in alternation.
The first argument will then be interpreted as the first key, the second argument as the first value, the third argument as the second key, and so on.
If you provide an odd number of arguments, the last value will default to ``{'$exists': true}``.

Querying via operator is supported using the ``.``-operator.
Finally, you can use ``/<regex>/`` instead of ``{'$regex': '<regex>'}`` for regular expressions.

The following list shows simplified ``signac find`` expressions on the left, full query syntax in Python in the middle, and full query syntax in JSON on the right.

.. code-block:: bash

    simplified            full Python                           full JSON
    -------------------  ------------------------------------  --------------------------------
    p                    {'p': {'$exists': True}}              '{"p": {'$exists': true}}'
    p 2                  {'p': 2}                              '{"p": 2}'
    p 2 kT               {'p': 2, 'kT': {'$exists': True}}     '{"p": 2, "kT": {"$exists": true}}'
    p 2 kT.$gte 1.0      {'p': 2, 'kT': {'$gte': 1.0}}         '{"p": 2, "kT.": 1.0}'
    protocol /assembly/  {'protocol': {'$regex': 'assembly'}}  '{"protocal": {"$regex": "assembly"}}'

.. important::

    The ``$`` character used in operator-expressions must be escaped in many terminals, that means for example instead of ``$ signac find p.$gt 2``, you would need to write ``$ signac find p.\$gt 2``.
