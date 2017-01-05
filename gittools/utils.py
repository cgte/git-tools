# coding: utf-8

def one(iterable):
    content = list(iterable)
    if len(iterable) != 1:
        raise ValueError("More than one element in %r" % content)
    return content[0]

