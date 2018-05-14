def foo_is_odd(job):
    print(job.sp.foo, 'even' if job.sp.foo % 2 else 'odd')


if __name__ == '__main__':
    import signac
    project = signac.get_project()
    for job in project:
        foo_is_odd(job)
