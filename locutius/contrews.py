from collections import namedtuple
from locutius.multimethods import *
import builtins


Atom = namedtuple('Atom', ['ob'])
# Integer is just int
# Real is just float
Number = namedtuple('Number', ['ob'])
# String is just str
# Complex is just complex


class Symbol(str):
    """Just established a Python type for Symbols"""


Expression = namedtuple('Expression', ['head', 'args'])
List = namedtuple('List', ['args'])


@method(Number)
def rewrite(number):
    return builtins.eval(str(number.ob))


@method(complex)
def rewrite(c):
    return c


@method(float)
def rewrite(f):
    return f


@method(int)
def rewrite(i):
    return i


__contrews_global_rewrite_table__ = {}


@method(Symbol)
def rewrite(symbol):
    val = __contrews_global_rewrite_table__.get(symbol, symbol)
    return val


@method(Symbol)
def set(symbol, val):
    __contrews_global_rewrite_table__[symbol] = val