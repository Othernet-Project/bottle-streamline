import pytest

from streamline import utils as mod


MOD = mod.__name__


@pytest.mark.parametrize('s,out', [
    ('FooBar', 'foo_bar'),
    ('FOOBar', 'foobar'),
    ('FooBAR', 'foo_bar'),
    ('FooBARBaz', 'foo_barbaz'),
])
def test_decamelize(s, out):
    assert mod.decamelize(s) == out
