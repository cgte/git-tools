from subprocess import check_output as c


def hash(ref='HEAD'):
    return c(f'git rev-parse {ref}', shell=True).decode('utf-8').split('\n')[0]

def ref_in_branch(ref='HEAD', remote='', branch='master')
    if remote:
        branch = '{remote}/{branch}'
    cmd = f"git branch -a --contains {ref} | sed 's:remotes/::' | cut -c 3-"
    contains = set(c(cmd, shell=True).decode('utf-8').split('\n'))
    return branch in contains


