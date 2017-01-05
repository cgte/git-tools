#!/usr/bin/python

"""
This module aims to automatically rebase unmerged branch onto target branch.
Goals:
        Nicer commit tree
        Save your time

"""

import sys, shlex
from subprocess import check_call, CalledProcessError

from gitcmd import sync_branch, unmerged,  broader_than, goback

import argparse

import logging as log

parser = argparse.ArgumentParser('Automatic rebaser')
parser.add_argument('--target-branch', '-t', default='master',
                    help="name of the branch to rebase onto"
                    )
parser.add_argument('--sync-target', '-s', action='store_const',
                    const=False, default=True,
                    help="Pulls and pushes the target "
                         "branch prior to rebasing")
parser.add_argument('--branch', '-b', default=None,
                    help="specify only one branch to rebase")


def shouldnot_rebase_branch(branch_name):
    return 'norebase' in branch_name


def main(params=''):
    params = vars(parser.parse_args(shlex.split(params))) if params else vars(parser.parse_args())
    autorebase(**params)


@goback
def autorebase(target_branch, sync_target, branch):
    if sync_target:
        sync_branch(target_branch)
    diverged = unmerged(branch=target_branch)
    log.warn("Diverged \n %r" % list(diverged))
    broader = broader_than(branch=target_branch)
    log.warn("Broader \n %r" % list(broader))

    to_rebase = diverged - broader if not branch else [branch, ]

    log.info('branches to be rebased: %s',  ' ,'.join(to_rebase))

    failed, success = [], []
    sys.stdout.flush()
    for branch in to_rebase:
        if shouldnot_rebase_branch(branch):
            continue
        log.info('rebasing %s', branch)
        try:
            check_call(['git rebase %s %s' % (target_branch, branch)],
                       shell=True)
            success.append(branch)
        except CalledProcessError:
            check_call(['git rebase --abort'], shell=True)
            failed.append(branch)

    return {'failed': failed, 'succeeded': success}


if __name__ == '__main__':
    print(main())
