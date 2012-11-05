from altered import Expando

def test_falsy_when_new():
    assert not Expando()

def test_falsy_on_change():
    exp = Expando(x='y')
    del exp.x
    assert not exp

def test_truthy_when_new():
    assert Expando(content='something') and True or False

def test_truthy_on_change():
    exp = Expando()
    exp.x = 'y'
    assert exp
