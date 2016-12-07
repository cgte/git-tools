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
        self.repodir = join(directory, 'repo_rebase_testbase_%s' % rand())
        os.mkdir(self.repodir)

    def test_base(self):
        os.chdir(self.repodir)
        target = 'targetbranch'
        statements = ['git init ',
                      'git checkout -b %s' % target,
                      'touch file1',
                      'git add file1',
                      "git commit -m 'add file1' file1",
                      "echo 'abce' > file1",
                      "git commit -m 'fill file1' file1",
                      "git checkout HEAD^",
                      'git checkout -b branch_to_rebase',
                      "echo 'abce' > file2",
                      "git add file2",
                      "git commit -m 'add file to be rebased'",
                      # Go back on working branch
                      "git checkout %s" % target,
                      "git checkout -b broader",
                      "echo 'some content' >> file1 ",
                      "git commit -m 'some heavy work on file 1' file1"
                      ]
        for statement in statements:
            check_call(statement, shell=True, stdout=devnull, stderr=devnull)

        self.assertEqual(one(gitcmd.broader_than(target)), 'broader')

        self.assertEqual(gitcmd.unmerged(target), set(['broader', 'branch_to_rebase']))

        self.assertEqual(one(gitcmd.unmerged(target) - gitcmd.broader_than(target)), 'branch_to_rebase')

    def tearDown(self):
        from time import sleep
        sleep(2)
        check_call('rm -rf %s' %  self.repodir, shell=True)

if __name__ == '__main__':
    main()

