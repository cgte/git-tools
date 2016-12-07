#!/usr/bin/python

"""
This module aims to automatically rebase unmerged branch onto target branch.
Goals:
        Nicer commit tree
        Save your time

"""

import sys
from subprocess import check_call, CalledProcessError

from gitcmd import update_branch, unmerged,  broader_than


def shouldnot_rebase_branch(branch_name):
    return 'norebase' in branch_name


def main(target='master', update_target=True):
    if update_target:
        update_branch(target)
    diverged = unmerged(branch=target)

    broader = broader_than(branch=target)

    to_rebase = diverged - broader

    print 'branches to be rebased: ', ' ,'.join(to_rebase)

    failed, success = [], []
    sys.stdout.flush()
    for branch in to_rebase:
        if shouldnot_rebase_branch(branch):
            continue
        try:
            check_call(['git rebase %s %s' % (target, branch)],
                       shell=True)
            success.append(branch)
        except CalledProcessError:
            check_call(['git rebase --abort'], shell=True)
            failed.append(branch)

    return {'failed': failed, 'succeeded': success}


if __name__ == '__main__':
    main()
