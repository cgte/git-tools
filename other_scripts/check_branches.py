from functools import partial
from subprocess import run
import datetime

_shell = partial(run, **{"shell": True, "encoding": "utf-8", "capture_output": True})


long_live_branches = ["main", "master"]


def stripper(text):
    """
    >>> s = '''
    ... a
    ...
    ... b
    ... '''
    >>> stripper(s)
    ['a', 'b']

    """

    return [
        line
        for line in filter(None, map(lambda x: x.strip(), text.strip().split("\n")))
    ]


def list_merged_branches(ref="main"):

    merged_branches = _shell(f"git branch --merged {ref} | grep -v '^\*'")
    branch_names = stripper(merged_branches.stdout)

    return [b for b in branch_names if b not in long_live_branches]


def remote_branches(remote="origin"):
    this_remote_only = f" grep '{remote}/'"
    remotes = f"git branch -r | {this_remote_only} "
    out = _shell(remotes)
    breakpoint()


def is_synced_with_origin(branch_name, origin="origin"):
    sync = _shell(f"git diff {branch_name} {origin}/{branch_name}")
    out = sync.stdout
    if out:
        print(out)
    return not out


branches = list_merged_branches()

branches_to_remove = []

branches_to_sync = []

for b in branches:
    if is_synced_with_origin(b):
        print(f"{b} can be deleted")
        branches_to_remove.append(b)
    else:
        branches_to_sync.append(b)

commands = []

import datetime


def get_date(ref):
    out = _shell(f'git show --format="%ad" --date=short --no-patch {ref}')
    try:
        date = datetime.date(*map(int, out.stdout.split("-")))
    except:
        breakpoint()
    return date


def older_than_a_week(branch, date=None):
    if date is None:
        date = datetime.date.today()
    bdate = get_date(branch)
    return (date - bdate).days > 7


def has_remote_counterpart(branch, remote="origin"):
    out = _shell(f"git ls-remote --heads {remote} {branch}")
    return out.stdout


for rm_remote in branches_to_remove:
    rm_origin = f"git push origin :{rm_remote}"
    dte = get_date(rm_remote)
    more_than_a_week = older_than_a_week(rm_remote)
    has_remote = has_remote_counterpart(rm_remote)
    print(
        f"{rm_remote} {dte} is{ '' if  more_than_a_week else ' not'} older than a week"
    )
    print(f"{rm_remote} has is{ '' if  has_remote else ' no'} remote counterpart")

    if more_than_a_week:

        if has_remote:
            commands.append(rm_origin)
        else:
            commands.append(f"git branch -D {rm_remote}")


print("\n".join(commands))


def remote_unmerged(remote="origin", ref="main"):
    out = _shell(f"git branch -r --no-merged  {remote}/{ref}")
    branches = stripper(out.stdout)
    return branches


def derivate_from(derivative, reference):
    derivates = f"git branch -a {derivative} --contains {reference}"
    out = _shell(derivates)
    return out.stdout


remotes = remote_unmerged()

for reference in remotes:

    shortname = reference.split("/")[-1]

    command = f"git checkout {shortname}"

    is_main_derivate = derivate_from(reference, "origin/main")

    print(f"{reference} seems {'up to' if is_main_derivate else 'out of'} date")
    if not is_main_derivate:
        print(command)
        print("git rebase  main")
        print("git push -f")
