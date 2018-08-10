"""Adapted from Adam Bard's work at https://unpythonic.com/02_02_multimethods/,
with clarifications, corrections, and unit tests."""

#   ___                       _                   _
#  / __|___ _ _  ___ _ _ __ _| |  __ __ _ ___ ___(_)
# | (_ / -_) ' \/ -_) '_/ _` | | / _/ _` (_-</ -_)_
#  \___\___|_||_\___|_| \__,_|_| \__\__,_/__/\___(_)
#  ___  _               _      _                 __   __    _
# |   \(_)____ __  __ _| |_ __| |_ ___ ___ _ _ __\ \ / /_ _| |_  _ ___
# | |) | (_-< '_ \/ _` |  _/ _| ' \___/ _ \ ' \___\ V / _` | | || / -_)
# |___/|_/__/ .__/\__,_|\__\__|_||_|  \___/_||_|   \_/\__,_|_|\_,_\___|
#           |_|


def multi(get_dispatch_value):
    """Decorate a function 'get_dispatch_value' with a dispatch table, initially
    empty. The decorated function is used later when multimethods with the same
    name as the actual argument of multi are applied to arguments.

    By example: the common case of dispatch-on-type:

    >>> Circle = namedtuple('Circle', ['radius'])
    ...
    ... @multi
    ... def area_m(shape):
    ...     return type(shape)

    The decorated function 'area_m' becomes 'get_dispatch_value.' Later, the
    same name is used to define a multimethod for some type, 'Circle', and
    for another type, 'Square':

    >>> @multimethod(area_m, Circle)  # <~~~ the 'multi' is specified here
    ... def area_m(circle):           # <~~~ note the same name 'area_m'
    ...     return circle.radius ** 2 * PI
    ...
    ... @multimethod(area_m, Square)  # <~~~ the 'multi' is specified here
    ... def area_m(square):           # <~~~ same name, 'area_m'
    ...     return square.side ** 2   # <~~~ different function body

    The next example shows a dispatch function that looks up an arbitrarily
    named dispatch key in a dictionary -- you can dispatch on anything, not
    just types:

    >>> @multi
    ... def area_d(shape):
    ...     return shape['dispatch-key']

    """
    def _multi_inner(*args, **kwargs):
        dispatching_value = get_dispatch_value(*args, **kwargs)
        dispatched_to_fn = _multi_inner.__multi__.get(
            dispatching_value,
            _multi_inner.__multi_default__  # Default on missing key
        )
        result = dispatched_to_fn(*args, **kwargs)  # apply it NOW!
        return result

    _multi_inner.__multi__ = {}  # initially empty ...

    # except for this None-returning, constant, default default function

    _multi_inner.__multi_default__ = lambda *args, **kwargs: None

    return _multi_inner


def multimethod(previous_multi=None, dispatch_key=None):
    """Decorate a target function f by adding an entry {k: f} to the dispatch table
    of 'previous_multi', where k is 'dispatch_key'.

    Use 'dispatch_key=None' to set a default multimethod for f. That default
    will be invoked when f is called with a dispatch_key that isn't in the
    dispatch table of previous_multi.

    Don't apply a multimethod decoration without arguments; results are undefined.

    Don't apply a multimethod decoration with previous_multi that isn't
    actually a previous multi; results are undefined.

    The following example illustrates the common case of dispatch-on-type,
    using the types automatically generated by collections.namedtuple, a
    standard type constructor:

    >>> Circle = namedtuple('Circle', ['radius'])
    ...
    ... @multi
    ... def area_m(shape):
    ...     return type(shape)
    ...
    ... @multimethod(area_m, Circle)
    ... def area_m(circle):
    ...     return circle.radius ** 2 * PI

    """
    def apply_decorator(f):
        if dispatch_key is None:
            previous_multi.__multi_default__ = f
        else:
            previous_multi.__multi__[dispatch_key] = f
        return previous_multi

    return apply_decorator


#   ___                                            _
#  / __|___ _ __  _ __  ___ _ _    __ __ _ ___ ___(_)
# | (__/ _ \ '  \| '  \/ _ \ ' \  / _/ _` (_-</ -_)_
#  \___\___/_|_|_|_|_|_\___/_||_| \__\__,_/__/\___(_)
#  ___  _               _      _                  _____
# |   \(_)____ __  __ _| |_ __| |_ ___ ___ _ _ __|_   _|  _ _ __  ___
# | |) | (_-< '_ \/ _` |  _/ _| ' \___/ _ \ ' \___|| || || | '_ \/ -_)
# |___/|_/__/ .__/\__,_|\__\__|_||_|  \___/_||_|   |_| \_, | .__/\___|
#           |_|                                        |__/|_|


# Here is a shortcut 'method' that implements dispatch-on-type in one
# decoration. See 'test_multimethods.py' for in-depth usage examples.


__locutius_multimethods__ = {}


def method(some_type, *args):
    """Replace another function f with a multimethod bound to 'some_type.' This is
    a one-step alternative to the two-step procedure of declaring a multi and
    then defining a multimethod with that multi and a type.

    The purpose of 'method' is to bind the NAME of f to some_type. We want to
    end up with multiple functions for different types, all with the same
    names.

    Say we're decorating a function named 'area' and binding it to the type
    'Circle', as follows:

    >>> @method(Circle)
    ... def area(circle):
    ...     return circle.radius ** 2 * PI

    When the new, decorated 'area' is called with a Circle as argument, as in

    >>> area(Circle(radius=42))

    a dispatch table is consulted with the type of the argument, namely
    'Circle', and the resulting multimethod 'area' is called.

    Don't decorate a function without a type argument to 'method'. Results are
    undefined:

    >>> @method
    ... def dont_try_this():
    ...     return None

    """

    def get_dispatch_value(t, *args, **kwargs):
        """Fixed function returning type."""
        return type(t)

    def not_implemented(*args, **kwargs):
        """Agressive default multimethod for 'method'."""
        raise NotImplementedError("Method not implemented for %s" % \
                                  get_dispatch_value(*args, **kwargs))

    def _method_inner(fn):
        # Search for existing multi
        nym = fn.__name__
        previous_multi = __locutius_multimethods__.get(nym, None)

        if previous_multi is None or not hasattr(previous_multi, '__multi__'):

            # Make the multi if it doesn't exist or doesn't have a dispatch
            # table:

            previous_multi = multi(get_dispatch_value)

            # Call multimethod with some_type == None just to set the
            # aggressive default:

            previous_multi = multimethod(previous_multi)(not_implemented)

            # Store the name of the multi in a global

            __locutius_multimethods__[nym] = previous_multi

        # In any case, call 'multimethod' with the supplied type:

        return multimethod(previous_multi, some_type)(fn)

    return _method_inner
