
from .main import bar, bingo, bango


def test_bar():
    assert bar() == 99

def test_bingo():
    pass
    # assert bingo() == 2

def test_bango():
    bango(False)

