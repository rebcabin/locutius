from locutius.contrews import *
from unittest import TestCase


class TestExpressions(TestCase):
    """"""
    def setUp(self):
        pass

    def test_constants(self):
        c1 = Number("42")
        assert rewrite(c1) == 42
        c2 = Number(42)
        assert rewrite(c2) == 42
        c3 = 4 + 2j
        assert rewrite(c3) == 4 + 2j
        c4 = 42
        assert rewrite(c4) == 42
        c5 = 42.0
        assert rewrite(c5) == 42.0

    def test_set_of_symbol(self):
        assert rewrite(Symbol("foo")) == "foo"
        set(Symbol("foo"), 42)
        assert rewrite(Symbol("foo")) == 42


def test_test_itself():
    assert True
