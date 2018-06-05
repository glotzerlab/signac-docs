from sacred import Experiment

ex = Experiment()


@ex.main
def hello(foo):
    print('hello', foo)


if __name__ == '__main__':
    ex.run_commandline()
