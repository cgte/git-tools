#coding: utf-8
"""
I have multiples repos i may want to sync.

#TODO: Try to be smart abour letting repos i am wokring on in the same state.
"""



from subprocess import CalledProcessError
import os
from gitcmd import has_diff, backandforth, pull, push, fetch, origin_diff
import sys

def main():

    try:
        path = sys.argv[1]
    except IndexError:
        path = os.getcwd()

    path = os.path.abspath(os.path.expanduser(path))

    git_repos = []
    for x in os.listdir(path):
        repopath = os.path.join(path, x)
        if os.path.isdir(os.path.join(repopath, '.git')):
            git_repos.append(repopath)

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

    for repo in git_repos:
        if is_gitsvn(repo):
            print repo, 'is a git svn repo not handled yet' # The is an origin, remote issue
            continue
        os.chdir(repo)
        with backandforth():
            print repo
            fetch()
            if repo not in upgradable_repos:
                continue
            try:
                if origin_diff():
                    print 'pulling master'
                    pull('master')
                if not push():
                    print '#####################################'
                    print 'push failed for'
                    print os.getcwd()
            except Exception as e:
                print e
                continue
    os.chdir(here)


if __name__ == '__main__':
    main()
