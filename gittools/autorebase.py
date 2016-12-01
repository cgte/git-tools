#!/usr/bin/python

from subprocess import check_output, check_call, CalledProcessError

print check_output(['git checkout master && git pull'], shell=True)


diverged = check_output(['git branch --no-merged master'], shell=True).split()


# List branches and removes star on current one

diverged = set([s for s in [s.strip(' *\n') for s in diverged ] if s])

print diverged

broader = check_output(['git branch --contains master'],
                        shell=True).split()

broader = set([s for s in [s.strip(' *\n') for s in broader ] if s])

print broader

to_rebase = diverged - broader

print 'branches to be rebased: ', ' ,'.join(to_rebase)

failed = []
import sys
sys.stdout.flush()
for branch in to_rebase:
    if 'bckup' in branch:
        continue
    try:
        out = check_output(['git rebase master %s' % branch], shell=True)
        print out
        print ''
    except CalledProcessError :
        check_call(['git rebase --abort'],shell=True)
        print 'please fix'
        failed.append(branch)
        break

print 'failed ', failed if failed else None

