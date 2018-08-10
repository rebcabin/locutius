from locutius.contrews import *
from unittest import TestCase


class TestExpressions(TestCase):
    """"""
    def setUp(self):
        pass

    def test_atom_eval(self):
        c3 = 4 + 2j
        assert rewrite(c3) == 4 + 2j
        c4 = 42
        assert rewrite(c4) == 42
        c5 = 42.0
        assert rewrite(c5) == 42.0
        c7 = "foobar"
        assert rewrite(c7) == "foobar"

        assert rewrite(Symbol("foo")) == Symbol("foo")
        # A Symbol and its string representation are identical.
        # TODO: Is this a good idea?
        assert rewrite(Symbol("foo")) == "foo"

    def test_heads(self):
        c3 = 4 + 2j
        assert head(c3) == "Complex"
        c4 = 42
        assert head(c4) == "Integer"
        c5 = 42.0
        assert head(c5) == "Real"
        c7 = "foobar"
        assert head(c7) == "String"

        assert head(Symbol("foo")) == "Symbol"

        assert head([1, 2, 3]) == "List"

    def test_set_of_symbol(self):
        set(Symbol("foo"), 42)
        assert rewrite(Symbol("foo")) == 42

    def test_expr_rewrite(self):
        assert rewrite(Expression(Symbol('Plus'), [1, 2, 3])) == 6

def test_test_itself():
    assert True
