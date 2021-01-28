.. _examples:

========
Examples
========

Examples are provided as `Jupyter <https://jupyter.org/>`_ notebooks in a separate
`signac-examples <https://github.com/glotzerlab/signac-examples>`_ repository.
These notebooks may be launched `interactively on Binder <https://mybinder.org/v2/gh/glotzerlab/signac-examples/master?filepath=index.ipynb>`_
or downloaded and run on your own system.
Visualization of data is done via `Matplotlib <https://matplotlib.org/>`_ and `Bokeh <https://bokeh.pydata.org/>`_, unless otherwise noted.

This is a collection of example projects which are designed to illustrate how to implement certain applications and solutions with **signac**.
Unlike the tutorial, the examples consist mainly of complete, immediately executable source code with less explanation.

Key concepts
============

There are a few critical concepts, algorithms, and data structures that are central to all of **signac**.
The :class:`signac.box.Box` class defines the concept of a periodic simulation box, and the :mod:`signac.locality` module defines methods for finding nearest neighbors of particles.
Since both of these are used throughout **signac**, we recommend reading the :ref:`tutorial` first, before delving into the workings of specific **signac** analysis modules.

.. toctree::
    :maxdepth: 1
    :glob:

    signac-examples/notebooks/signac_1*

Example Analyses
================

The examples below go into greater detail about specific applications of **signac** and use cases that its analysis methods enable, such as user-defined analyses, machine learning, and data visualization.

