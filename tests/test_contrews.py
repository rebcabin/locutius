from locutius.contrews import *
from unittest import TestCase
import pytest


class TestExpressions(TestCase):
    """"""
    def setUp(self):
        pass

    def test_atom_eval(self):
        c3 = 4 + 2j
        with pytest.raises(NotImplementedError):
            assert rewrite(c3) == 4 + 2j
        c4 = 42
        with pytest.raises(NotImplementedError):
            assert rewrite(c4) == 42
        c5 = 42.0
        with pytest.raises(NotImplementedError):
            assert rewrite(c5) == 42.0
        c7 = "foobar"
        with pytest.raises(NotImplementedError):
            assert rewrite(c7) == "foobar"

        assert rewrite(Symbol("foo")) == Symbol("foo")

        assert rewrite(Symbol("foo")) != String("foo")

    def test_heads(self):
        c3 = 4 + 2j
        assert head(c3) == Symbol("Complex")
        c4 = 42
        assert head(c4) == Symbol("Integer")
        c5 = 42.0
        assert head(c5) == Symbol("Real")
        c7 = "foobar"
        assert head(c7) == Symbol("String")

        assert head(Symbol("foo")) == Symbol("Symbol")

        assert head([1, 2, 3]) == Symbol("List")

    def test_set_of_symbol(self):
        set(Symbol("foo"), 42)
        assert rewrite(Symbol("foo")) == 42

    def test_expr_rewrite(self):
        assert rewrite(
            Expression(
                Symbol('Plus'),
                [Integer(i) for i in [1, 2, 3]])) == 6

    def test_number_q(self):
        assert number_q(Integer(42))
        assert number_q(Real(42.0))
        assert number_q(Complex(4 + 2j))
        assert not number_q("foobar")
        assert not number_q(Symbol("Whatever"))

def test_test_itself():
    assert True
