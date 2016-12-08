# coding: utf-8
"""
Simple git commands

Note: improve later using advice : http://stackoverflow.com/questions/3846380/

"""
from subprocess import check_output


def clean_lines_star_cr(branches_output_lines):
    # Clean git branch output so as to return names.
    # the right approach would be to use git plumbing instead of porcelain
    temp = [s.strip(' *\n') for s in branches_output_lines]
    temp = set([s for s in temp if s])
    return temp


def sync_branch(branch_name):
    print check_output(['git checkout %s && git pull && git push' %
                        branch_name], shell=True)


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
