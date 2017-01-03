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

from gittools import gitcmd

directory = abspath(dirname(__file__))

devnull = open(os.devnull, 'w')

def one(iterable):
    content = list(iterable)
    if len(iterable) != 1:
        raise ValueError("More than one element in %r" % content)
    return content[0]

def rand(N=4):
    return str(randint(0, 10**N)).zfill(N)


class DefaultTestCase(TestCase):
    """
    Creates a branch, rewind
    """


    def setUp(self):
        self.repodir = join(directory, 'repo_cmd_testbase_%s' % rand())
        os.mkdir(self.repodir)
        os.chdir(self.repodir)
        check_call('git init .', shell=True)

    def test_branch(self):

        statements = ['git init ',
                      'touch file1',
                      'git add file1',
                      "git commit -m 'add file1' file1",
                      ]
        for statement in statements:
            check_call(statement, shell=True, stdout=devnull, stderr=devnull)

        name = 'plop'
        check_call('git checkout -b %s' % name, shell=True)
        with gitcmd.backandforth():
            name2 = 'plip'
            check_call('git checkout -b %s' % name2, shell=True)
            branch2 = gitcmd.current_branch()


        self.assertEqual(branch2, name2)
        self.assertEqual(gitcmd.current_branch(), name)




    def tearDown(self):
        os.chdir('..')
        check_call('rm -rf %s' %  self.repodir, shell=True)

if __name__ == '__main__':
    main()

