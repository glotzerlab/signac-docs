.. _dashboard:

The Dashboard
=============

This chapter describes how to create a dashboard to quickly visualize data stored in a **signac** data space.
To install the **signac-dashboard** package, see :ref:`dashboard-installation`.

.. danger::

    As with any web server, be aware of the :ref:`dashboard-security`.

Getting Started
---------------

You can start a dashboard to visualize **signac** project data in the browser, by importing the :py:class:`~signac_dashboard.Dashboard` class and calling its :py:meth:`~signac_dashboard.Dashboard.main` method.

.. code-block:: python

    from signac_dashboard import Dashboard

    Dashboard().main()

Start a Dashboard
-----------------

The code below will open a dashboard for an newly-initialized (empty) project, with no jobs and one module loaded. Write the file ``dashboard.py`` with these contents:

.. code-block:: python

    from signac_dashboard import Dashboard
    from signac_dashboard.modules import ImageViewer

    if __name__ == "__main__":
        Dashboard(modules=[ImageViewer()]).main()

Then launch the dashboard with ``python dashboard.py run``.

Included Modules
----------------

For a list of available modules and usage instructions, see :ref:`python-api-dashboard-modules`.

Specifying a custom job title
-----------------------------

By creating a class that inherits from :py:class:`~signac_dashboard.Dashboard` (which we'll call ``MyDashboard``), we can begin to customize some of the functions that make up the dashboard, like :py:meth:`~signac_dashboard.Dashboard.job_title`, which gives a human-readable title to each job.

.. code-block:: python

    class MyDashboard(Dashboard):
        def job_title(self, job):
            return "Concentration(A) = {}".format(job.sp["conc_A"])


    if __name__ == "__main__":
        MyDashboard().main()

.. _dashboard-remote-ssh:

Running dashboards on a remote host
-----------------------------------

To use dashboards hosted by a remote computer, open an SSH tunnel to the remote computer and forward the port where the dashboard is hosted. For example, connect to the remote computer with

.. code-block:: bash

    ssh username@remote.server.org -L 8890:localhost:8888

to forward port 8888 on the host to port 8890 on your local computer.

The process looks like this:

1. Open an SSH connection to the remote server with a forwarded port using a command like the one shown above.
2. Launch signac-dashboard on the remote server, using the remote port you forwarded (port 8888 in the example above).
3. On your local computer, open your browser to the local port (this is ``http://localhost:8890`` in the example above).

Dissecting the Dashboard Structure
----------------------------------

- *Jobs* are how **signac** manages data. Each job has a statepoint (which contains job metadata) and a document (for persistent storage of key-value pairs). Jobs can be displayed in *list view* or *grid view*. The list view provides quick descriptions and status information from many jobs, while the grid view is intended to show text and media content from one or more jobs.
- *Templates* provide the HTML structure of the dashboard's pages, written in Jinja template syntax for rendering content on the server
- *Modules* are server-side Python code that interface with your **signac** data to display content. Generally, a module will render content from a specific *job* into a *card template*.
- *Cards* are a type of template that is shown in *grid view* and contains content rendered by a *module*.

Searching jobs
--------------

The search bar accepts JSON-formatted queries in the same way as the ``signac find`` command-line tool. For example, using the query ``{"key": "value"}`` will return all jobs where the job statepoint ``key`` is set to ``value``. To search jobs by their document key-value pairs, use ``doc:`` before the JSON-formatted query, like ``doc:{"key": "value"}``.
