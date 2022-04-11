
from .main import bar, bingo, bango, foo, hello

def test_foo():
    foo()

def test_bar():
    assert bar() == 99

def test_bingo():
    assert bingo() == 2

def test_bango():
    bango(False)
    bango(True)



def test_hello():
    assert hello('dolly') == 'Mr. dolly'
