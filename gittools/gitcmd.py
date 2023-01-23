# coding: utf-8
"""
Simple git commands

Note: improve later using advice : http://stackoverflow.com/questions/3846380/

"""
from subprocess import check_output, check_call, Popen

from contextlib import contextmanager

from functools import wraps

import os
import logging as log

from .utils import silent, devnull

def goback(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        with backandforth():
            return function(*args, **kwargs)
    return wrapped


@contextmanager
def backandforth():
    """
    Put you back on the branch that were checked out when starting some work
    """
    initial_branch = current_branch()
    yield
    check_call('git checkout %s' % initial_branch, shell=True, **silent)


def branches(origin=False):
    if origin:
        branches = check_output("git branch -r | sed -s 's:origin/::' | cut -c 3-",
                                shell=True).split('\n')
    else:
        branches = check_output('git branch', shell=True).split('\n')

    branches = [b.strip(' *\n') for b in branches]
    branches = [b for b in branches if b]
    return branches

def current_branch():
    """
    Return current branch
    """
    branches = check_output('git branch', shell=True).split('\n')

    checked_out = [b.strip(' *\n') for b in branches
                   if b.startswith('*')]
    return checked_out[0]



def clean_lines_star_cr(branches_output_lines):
    # Clean git branch output so as to return names.
    # the right approach would be to use git plumbing instead of porcelain
    temp = [s.strip(' *\n') for s in branches_output_lines]
    temp = set([s for s in temp if s])
    return temp


def sync_branch(branch_name):
    #pull(branch_name)
    #push()
    output = check_output(['git checkout %s && git pull && git push' %
                           branch_name],
                          stderr=devnull,
                          shell=True)
    #log.info(output)

def pull(branch_name):
    #Bypass sync branch, smetimes you cannot push.
    available_branches =  branches()
    if branch_name not in available_branches:
        log.warn("No branch named %r skipping", branch_name)

    output = check_output(['git checkout %s && git pull' %
                           branch_name],
                          shell=True,
                          stderr=devnull)
    log.info(output)

def fetch():
    out = check_output(['git fetch origin'], shell=True)

def origin_diff():
    out = check_output(['git diff master origin/master'], shell=True)
    return out



def push():
    ret = None
    try:
        output = check_output('git push',
                              shell=True)
        log.info(output)
        ret = True
    except Exception as e:
        print(e)
        ret = False
    return ret

def unmerged(branch='master'):
    """ Returns branches names that are not conained in ``branch`` """
    tmp = check_output(['git branch --no-merged %s' % branch], shell=True)
    return clean_lines_star_cr(tmp.split())


def broader_than(branch='master'):
    """
    Returns branches that already contain master
    """
    tmp = check_output(['git branch --contains %s' % branch],
                       shell=True)
    return clean_lines_star_cr(tmp.split()) - set([branch])


def has_diff(path_to_repo=None):
    if path_to_repo:
        here = os.path.abspath(os.getcwd())
        os.chdir(path_to_repo)
    tmp = check_output(['git', 'diff', 'HEAD']).strip(' \n')
    if path_to_repo:
        os.chdir(here)
    return bool(tmp)


def clean_git_output(in_):
    ps = Popen("cut -c 3- |  sed 's:^remotes/::' | sed 's:^origin/::' "
               " | grep -v  '^master$' | grep -v '^HEAD' ",
               stdin=in_,
               shell=True)
    return ps.stdout

def unmerged2():
    ps = Popen(" git branch -a --no-merged 'master' ", shell=True)
    ps.wait()
    return ps.stdout

def branch_descending_latest_tags():
    ps = Popen(" git tag | sort -rV | sed '5q;d' | xargs git branch -a --contains ",
             shell=True)
    return ps.stdout

def rb():
    """
    Personal features, checks for features branches that have to be rebased
    This is useful for having a nice commit tree
    """




