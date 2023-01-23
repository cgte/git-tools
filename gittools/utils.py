# coding: utf-8


def one(iterable):
    content = list(iterable)
    if len(iterable) != 1:
        raise ValueError("More than one element in %r" % content)
    return content[0]


# this eases making silent system calls.
# We use the same file since we sometime use mock.assert_called_with

devnull = open("/dev/null", "w")
silent = {"stdout": devnull, "stderr": devnull}
