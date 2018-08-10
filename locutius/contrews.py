from collections import namedtuple
from locutius.multimethods import *
import builtins
import operator
from toolz import reduce

#  _____
# |_   _|  _ _ __  ___ ___
#   | || || | '_ \/ -_|_-<
#   |_| \_, | .__/\___/__/
#       |__/|_|


# Atoms are Integer, Real, Complex, String, and Symbol

# Integer is just built-in int
# Real is just built-in float
# Complex is just built-in complex
# String is just str


Symbol = namedtuple('Symbol', ['obj'])


class String(str):
    """Establish a Python type for contrews type 'String.'"""


Expression = namedtuple('Expression', ['head', 'expr_list'])


#                     _ _
#  _ _ _____ __ ___ _(_) |_ ___
# | '_/ -_) V  V / '_| |  _/ -_)
# |_| \___|\_/\_/|_| |_|\__\___|


__contrews_global_rewrite_table__ = {}


__contrews_global_rewrite_table__[Symbol('Plus')] = operator.add


@multi
def number_q(x):
    return type(x)


@multimethod(number_q)
def number_q(_):
    """Default value for number_q(x)."""
    return False


@multimethod(number_q, int)
def number_q(_):
    return True


@multimethod(number_q, float)
def number_q(_):
    return True


@multimethod(number_q, complex)
def number_q(_):
    return True


@method(Expression)
def rewrite(x):
    hd = rewrite(x.head)
    tl = [rewrite(a) for a in x.expr_list]
    if hd != x.head:
        return reduce(hd, tl)


@method(complex)
def rewrite(c):
    return c


@method(float)
def rewrite(f):
    return f


@method(int)
def rewrite(i):
    return i


@method(str)
def rewrite(s):
    return s


@method(Symbol)
def rewrite(symbol):
    val = __contrews_global_rewrite_table__.get(symbol, symbol)
    return val


#  _                _
# | |_  ___ __ _ __| |
# | ' \/ -_) _` / _` |
# |_||_\___\__,_\__,_|


@method(complex)
def head(_):
    return Symbol("Complex")


@method(str)
def head(_):
    return Symbol("String")


@method(int)
def head(_):
    return Symbol("Integer")


@method(float)
def head(_):
    return Symbol("Real")


@method(complex)
def head(_):
    return Symbol("Complex")


@method(Symbol)
def head(_):
    return Symbol("Symbol")


@method(list)
def head(_):
    return Symbol("List")


#          _
#  ___ ___| |_
# (_-</ -_)  _|
# /__/\___|\__|


@method(Symbol)
def set(symbol, val):
    __contrews_global_rewrite_table__[symbol] = val
