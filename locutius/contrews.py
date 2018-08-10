from collections import namedtuple
from locutius.multimethods import *
import builtins
import operator
import sys
from toolz import reduce

#  _____
# |_   _|  _ _ __  ___ ___
#   | || || | '_ \/ -_|_-<
#   |_| \_, | .__/\___/__/
#       |__/|_|


# Atoms are Integer, Real, Complex, String, and Symbol


class Integer(object):
    def __init__(self, obj):
        self.obj = obj
        self.order_key = 0


class Real(object):
    def __init__(self, obj):
        self.obj = obj
        self.order_key = 100


class Complex(object):
    def __init__(self, obj):
        self.obj = obj
        self.order_key = 200


class Symbol(object):
    def __init__(self, obj):
        self.obj = obj
        self.order_key = 300

    def __hash__(self):
        return ("Symbol" + self.obj).__hash__()

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.obj == other.obj
        else:
            return False


class String(object):
    """Establish a Python type for contrews type 'String.'"""
    def __init__(self, obj):
        self.obj = obj
        self.order_key = 400


Expression = namedtuple('Expression', ['head', 'expr_list'])


#                 _
#  _ _ _  _ _ __ | |__  ___ _ _ __ _
# | ' \ || | '  \| '_ \/ -_) '_/ _` |
# |_||_\_,_|_|_|_|_.__/\___|_|_\__, |
#                           |___| |_|


@multi
def number_q(x):
    return type(x)


@multimethod(number_q)
def number_q(_):
    """Default value for number_q(x)."""
    return False


@multimethod(number_q, Integer)
def number_q(_):
    return True


@multimethod(number_q, Real)
def number_q(_):
    return True


@multimethod(number_q, Complex)
def number_q(_):
    return True


#   ___                     _
#  / _ \ _ __  ___ _ _ __ _| |_ ___ _ _ ___
# | (_) | '_ \/ -_) '_/ _` |  _/ _ \ '_(_-<
#  \___/| .__/\___|_| \__,_|\__\___/_| /__/
#       |_|


def plus(a, b):
    result = 0
    return result


def reorder(l):
    result = 0
    return result


#                     _ _
#  _ _ _____ __ ___ _(_) |_ ___
# | '_/ -_) V  V / '_| |  _/ -_)
# |_| \___|\_/\_/|_| |_|\__\___|


__contrews_global_rewrite_table__ = {}


__contrews_global_rewrite_table__[Symbol('Plus')] = operator.add


@method(Expression)
def rewrite(x):
    hd = rewrite(x.head)
    tl = [rewrite(a) for a in x.expr_list]
    if hd != x.head:
        return reduce(hd, [t.obj for t in tl])


@method(Complex)
def rewrite(c):
    return c


@method(Real)
def rewrite(f):
    return f


@method(Integer)
def rewrite(i):
    return i


@method(String)
def rewrite(s):
    return s


@method(Symbol)
def rewrite(s):
    val = __contrews_global_rewrite_table__.get(s, s)
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
