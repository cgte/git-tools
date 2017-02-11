# coding:utf-8

"""
Create a repo and some branches. Then try to rebase the giverged ones.

"""


from unittest import TestCase, main


from contextlib import contextmanager

from subprocess import check_call

import mock


from os.path import splitext, abspath, dirname, join
import os

from gittools import gitcmd

from .utils import silent, rand, directory

#directory = abspath(dirname(__file__))


class CoverTestCase(TestCase):
    @mock.patch('gittools.gitcmd.check_output')
    def test_cover(self, mocked):

        #cover the sync branch system call
        gitcmd.sync_branch('master')
        mocked.assert_called_with(
            ['git checkout master && git pull && git push'],
            stderr=gitcmd.devnull,
            shell=True)


class DefaultTestCase(TestCase):
    """
    Creates a branch, rewind
    """


    def setUp(self):
        self.repodir = join(directory, 'repo_cmd_testbase_%s' % rand())
        os.mkdir(self.repodir)
        os.chdir(self.repodir)
        check_call('git init .', shell=True, **silent)

    def test_current_branch(self):

        statements = ['git init ',
                      'touch file1',
                      'git add file1',
                      "git commit -m 'add file1' file1",
                      ]
        for statement in statements:
            check_call(statement, shell=True, **silent)

        name = 'plop'
        check_call('git checkout -b %s' % name, shell=True, **silent)
        with gitcmd.backandforth():
            name2 = 'plip'
            check_call('git checkout -b %s' % name2, shell=True, **silent)
            branch2 = gitcmd.current_branch()


        self.assertEqual(branch2, name2)
        self.assertEqual(gitcmd.current_branch(), name)

    def test_branches(self):
        branches =  ['branch1', 'branch2']
        statements = ['touch file1',
                      'git add file1',
                      'git commit -m "add file 1"']
        for statement in statements:
            check_call(statement, shell=True, **silent)
        self.assertEqual(gitcmd.branches(), ['master'])
        created_branches = ['master']
        for branch in branches:
            check_call('git checkout -b %s' % branch, shell=True)
            created_branches.append(branch)
            self.assertEqual(sorted(created_branches),
                             sorted(gitcmd.branches())
                             )

    def test_diff(self):
        statements = ['git init ',
                      'touch file1',
                      'git add file1',
                      "git commit -m 'add file1' file1",
                      ]
        for statement in statements:
            check_call(statement, shell=True, **silent)

        self.assertFalse(gitcmd.has_diff('.'))

        #modifiy and chech for diff
        check_call('echo "plop" >> file1', shell=True)
        self.assertTrue(gitcmd.has_diff())
        check_call('git add file1', shell=True)

        os.chdir('..')

        self.assertTrue(gitcmd.has_diff(self.repodir))

        os.chdir(self.repodir)

        self.assertTrue(gitcmd.has_diff())

        check_call('git commit -m "PLop" file1', shell=True, **silent)

        self.assertFalse(gitcmd.has_diff())



    def tearDown(self):
        os.chdir('..')
        check_call('rm -rf %s' %  self.repodir, shell=True)

if __name__ == '__main__':
    main()

