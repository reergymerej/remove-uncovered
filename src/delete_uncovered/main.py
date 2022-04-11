def foo():
    print("not covered")


def bar():
    # covered
    return 99


def bingo():
    return 2


def bango(maybe: bool) -> None:
    """meh"""
    if maybe:
        print("horse")
    else:
        print("norse")


def hello(name):
    return f"Mr. {name}"


def dope():
    pass


def horse(s):
    if s:
        pass
    else:
        raise Exception()


def nope():
    return 99
