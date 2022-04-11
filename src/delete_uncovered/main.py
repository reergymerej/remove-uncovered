#!/usr/bin/env python

def foo():
    print('not covered')


def bar():
    # covered
    return 99

def bingo():
    pass

def bango(maybe: bool) -> None:
    """meh
    """
    if maybe:
        print('horse')
    else:
        print('norse')
