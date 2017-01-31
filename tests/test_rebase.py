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
from gittools import autorebase

from .utils import silent

directory = abspath(dirname(__file__))


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
        os.chdir(self.repodir)
        self.targetbranch = target = 'targetbranch'
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
            check_call(statement, shell=True, **silent)

    def test_base(self):
        target_branch = self.targetbranch

        self.assertEqual(one(gitcmd.broader_than(target_branch)), 'broader')

        self.assertEqual(gitcmd.unmerged(target_branch), set(['broader', 'branch_to_rebase']))

        branches_to_rebase = gitcmd.unmerged(target_branch) - gitcmd.broader_than(target_branch)

        self.assertEqual(one(branches_to_rebase), 'branch_to_rebase')

        rebase_result = autorebase.autorebase(target_branch=target_branch,
                                              branch=None)

        self.assertEqual(rebase_result['failed'], [])
        self.assertEqual(rebase_result['succeeded'], ['branch_to_rebase'])

        self.assertEqual(gitcmd.broader_than(target_branch), set(['branch_to_rebase', 'broader']))


    def test_command(self):
        #This test seems dirty to me ...
        target = self.targetbranch

        self.assertEqual(one(gitcmd.broader_than(target)), 'broader')

        self.assertEqual(gitcmd.unmerged(target), set(['broader', 'branch_to_rebase']))

        branches_to_rebase = gitcmd.unmerged(target) - gitcmd.broader_than(target)

        self.assertEqual(one(branches_to_rebase), 'branch_to_rebase')
        rebase_result = check_call('autorebase --target-branch=%s' % target, shell=True,
                                   **silent)


        self.assertEqual(gitcmd.broader_than(target), set(['branch_to_rebase', 'broader']))

    def test_cover_main(self):
        target = self.targetbranch

        autorebase.main('--target-branch=%s' % target)

        self.assertRaises(DeprecationWarning, autorebase.autorebase,
                          *[None, None], **{'sync_target':True})



    def tearDown(self):
        os.chdir('..')
        check_call('rm -rf %s' %  self.repodir, shell=True)

if __name__ == '__main__':
    main()

