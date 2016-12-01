#!/usr/bin/python

"""
This module aims to automatically rebase unmerged branch onto target branch.
Goals:
        Nicer commit tree
        Save your time

"""

import sys
from subprocess import check_output, check_call, CalledProcessError

from gitcmd import update_branch, diverged_from, broader_than


def shouldnot_rebase_branch(branch_name):
    return 'norebase' in branch_name


def main(branch='master', update_target=True):
    if update_target:
        update_branch(branch)
    diverged = diverged_from(branch=branch)

    broader = broader_than(branch=branch)

    to_rebase = diverged - broader

    print 'branches to be rebased: ', ' ,'.join(to_rebase)

    failed = []
    sys.stdout.flush()
    for branch_name in to_rebase:
        if shouldnot_rebase_branch(branch_name):
            continue
        try:
            out = check_output(['git rebase master %s' % branch], shell=True)
            print out
            print ''
        except CalledProcessError:
            check_call(['git rebase --abort'], shell=True)
            print 'please fix'
            failed.append(branch)
            break

    print 'failed ', failed if failed else None


if __name__ == '__main__':
    main()
