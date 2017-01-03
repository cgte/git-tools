#!/usr/bin/python

"""
This module aims to automatically rebase unmerged branch onto target branch.
Goals:
        Nicer commit tree
        Save your time

"""

import sys
from subprocess import check_call, CalledProcessError

from gitcmd import sync_branch, unmerged,  broader_than

import argparse

import logging as log

parser = argparse.ArgumentParser('Automatic rebaser')
parser.add_argument('--sync-target', '-s', action='store_true',
                    help="Pulls and pushes the target "
                         "branch prior to rebasing")
parser.add_argument('--target-branch', '-t', default='master',
                    help="name of the branch to rebase onto"
                    )

parser.add_argument('--branch', '-b', default=None,
                    help="specify only one branch to rebase")



def shouldnot_rebase_branch(branch_name):
    return 'norebase' in branch_name

def main():
     params = parser.parse_args()
     _main(target=params.target_branch, sync_target=params.sync_target,
           branch=params.branch)

def _main(target='master', sync_target=True, branch=None):
    if sync_target:
        sync_branch(target)
    diverged = unmerged(branch=target)
    log.warn("Diverged \n %r" % list(diverged))
    broader = broader_than(branch=target)
    log.warn("Broader \n %r" % list(broader))

    to_rebase = diverged - broader if not branch else [branch,]

    print 'branches to be rebased: ', ' ,'.join(to_rebase)

    failed, success = [], []
    sys.stdout.flush()
    for branch in to_rebase:
        if shouldnot_rebase_branch(branch):
            continue
        print 'rebasing ', branch
        try:
            check_call(['git rebase %s %s' % (target, branch)],
                       shell=True)
            success.append(branch)
        except CalledProcessError:
            check_call(['git rebase --abort'], shell=True)
            failed.append(branch)

    return {'failed': failed, 'succeeded': success}


if __name__ == '__main__':
    print(main())
