from random import randint

from os.path import abspath, dirname

from gittools.utils import silent, devnull

directory = abspath(dirname(__file__))


def rand(N=4):
    return str(randint(0, 10**N)).zfill(N)
