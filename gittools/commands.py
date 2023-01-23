from functools import partial
from subprocess import run


_shell = partial(run, **{"shell": True, "encoding": "utf-8", "capture_output": True})


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


def shell(*args, **kwargs):
    """ """
    out = _shell(*args, **kwargs).stdout
    lines = stripper(out)
    return out, lines


if __name__ == "__main__":
    run("ls")
    shell("ls")
