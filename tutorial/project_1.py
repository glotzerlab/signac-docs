def foo_is_odd(job):
    with job:
        with open('is_even.txt', 'w') as file:
            file.write('yes' if job.sp.foo % 2 else 'no')


if __name__ == '__main__':
    import signac
    project = signac.get_project()
    for job in project:
        foo_is_odd(job)
