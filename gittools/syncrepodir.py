#coding: utf-8
"""
I have multiples repos i may want to sync.

#TODO: Try to be smart abour letting repos i am wokring on in the same state.
"""



from subprocess import CalledProcessError
import os
from gitcmd import has_diff, backandforth, pull, push
import sys

try:
    import pdb
    pdb.set_trace()
    path = sys.argv[1]
    os.chdir(path)

except IndexError:
    sys.exit(1)


directories =  [os.path.abspath(x) for x in os.listdir(path) if os.path.isdir(x)]
git_repos = [directory for directory in directories if '.git' in os.listdir(directory) ]

upgradable_repos = [repo for repo in git_repos if not has_diff(repo)]

def is_gitsvn(repo=None):
    here =  os.getcwd()
    if repo:
        os.chdir(repo)
    res = os.path.exists('.git/svn')
    if repo:
        os.chdir(here)
    return res



from pprint import pprint
pprint(git_repos)
print '*' * 80
print 'Upgradable repo'
pprint(upgradable_repos)
print "repos with diff"
pprint(list(set(git_repos) - set(upgradable_repos)))

here = os.path.abspath(os.getcwd())

for repo in upgradable_repos:
    if is_gitsvn(repo):
        print repo, 'is a git svn repo not handled yet' # The is an origin, remote issue

        continue
    os.chdir(repo)
    with backandforth():
        print repo
        try:
            pull('master')
        except Exception as e:
            print e
            continue
        if not push():
            print '#####################################'
            print 'push failed for'
            print os.getcwd()
os.chdir(here)
