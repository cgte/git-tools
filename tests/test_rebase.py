# coding:utf-8

"""
Create a repo and some branches. Then try to rebase the giverged ones.

"""


from unittest import TestCase, main

from random import randint

from contextlib import contextmanager

from subprocess import check_call


from os.path import splitext, abspath, dirname, join
import os

print __name__, __file__
print splitext(__file__)
directory = abspath(dirname(__file__))

print directory




def rand(N=4):
    return '0000'
    return str(randint(0, 10**N)).zfill(N)


class DefaultTestCase(TestCase):
    """
    Creates a branch, rewind
    """


    def setUp(self):
        self.repodir = join(directory, 'repo_rebase_testbase_%s' % rand())
        check_call('rm -rf %s' %  self.repodir, shell=True)
        os.mkdir(self.repodir)

    def test_base(self):
        os.chdir(self.repodir)
        statements = ['git init ',
                      'git checkout -b targebranch',
                      'touch file1',
                      'git add file1',
                      "git commit -m 'add file1' file1",
                      "echo 'abce' > file1",
                      "git commit -m 'fill file1' file1",
                      "git checkout HEAD^",
                      'git checkout -b testbranch',
                      "echo 'abce' > file2",
                      "git add file2",
                      "git commit -m 'add file to be rebased'",
                      ]
        print os.getcwd()
        for statement in statements:
            print repr(statement)
            check_call(statement, shell=True)


if __name__ == '__main__':
    main()

