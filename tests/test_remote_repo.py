# coding: utf-8
"""
Test for functions that interract with remote repositories.
"""

import os

from unittest import TestCase
from os.path import join
from subprocess import check_call

from gittools import gitcmd

from .utils import rand, silent, directory



class RepoWithRemoteTestCase(TestCase):

    def setUp(self):
        self.workingdir = join(directory, 'repo_with_remote_%s' % rand())
        os.mkdir(self.workingdir)
        os.chdir(self.workingdir)

        check_call('git init remote', shell=True, **silent)

        self.gotoremote()
        check_call('echo "plop" > file1', shell=True)
        check_call('git add file1', shell=True)
        check_call('git commit -m "Add file1" file1', shell=True)

        self.gotodir()
        check_call('git clone remote local', shell=True)

    def gotodir(self):
        os.chdir(self.workingdir)

    def gotoremote(self):
        os.chdir(join(self.workingdir, 'remote'))

    def gotolocal(self):
        os.chdir(join(self.workingdir, 'local'))

    def test_simple_pull(self):

        # prepare some stuff on remote
        self.gotoremote()
        check_call('git checkout -b "feature_branch" ', shell=True)
        #back to master to allow pushing on non bare repo
        check_call('git checkout master ', shell=True)


        #coverage only, nowhere to push to
        self.assertFalse(gitcmd.push())

        self.gotolocal()
        gitcmd.fetch()
        self.assertEqual(gitcmd.branches(), ['master'])

        gitcmd.pull("feature_branch")

        self.assertEqual(sorted(gitcmd.branches()), ['feature_branch',
                                                     'master'])

        check_call('git commit --allow-empty -m "empty push commit"', shell=True)

        gitcmd.origin_diff()  # cover

        gitcmd.push()





    def tearDown(self):
        os.chdir(self.workingdir)
        os.chdir('..')
        check_call('rm -rf %s' %  self.workingdir, shell=True)





