# coding:utf-8

"""
Create a repo and some branches. Then try to rebase the giverged ones.

"""


from unittest import TestCase, main

from random import randint

from contextlib import contextmanager

from subprocess import check_call

import mock


from os.path import splitext, abspath, dirname, join
import os

from gittools import gitcmd

directory = abspath(dirname(__file__))

devnull = open(os.devnull, 'w')

def rand(N=4):
    return str(randint(0, 10**N)).zfill(N)


class CoverTestCase(TestCase):
    @mock.patch('gittools.gitcmd.check_output')
    def test_cover(self, mocked):

        #cover the sync branch system call
        gitcmd.sync_branch('master')
        mocked.assert_called_with(
            ['git checkout master && git pull && git push'],
            shell=True)

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

    def test_diff(self):
        statements = ['git init ',
                      'touch file1',
                      'git add file1',
                      "git commit -m 'add file1' file1",
                      ]
        for statement in statements:
            check_call(statement, shell=True, stdout=devnull, stderr=devnull)

        self.assertFalse(gitcmd.has_diff())

        #modifiy and chech for diff
        check_call('echo "plop" >> file1', shell=True)
        self.assertTrue(gitcmd.has_diff())
        check_call('git add file1', shell=True)
        self.assertTrue(gitcmd.has_diff())

    def tearDown(self):
        os.chdir('..')
        check_call('rm -rf %s' %  self.repodir, shell=True)

if __name__ == '__main__':
    main()

