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
    """Decorates a function with a dispatch table, initially empty. The input
    'get_dispatch_value' is saved (closed-over) and used later when
    'multimethod's with the same name as the 'multi' are applied to arguments.
    The built-in decorator mechanism replaces the decorated function with the
    closure '_multi_inner'.

    If the argument 'get_dispatch_value' is not explicity supplied, then it is
    taken as the decorated function.

    The following example illustrates the common case of dispatch-on-type:

    >>> @multi
    ... def area_m(shape):
    ...     return type(shape)

    The next example shows an arbitrary dispatch key

    >>> @multi
    ... def area_d(shape):
    ...     return shape['dispatch-key']

    See 'test_locutius.py' for in-depth usage examples.

    """
    def _multi_inner(*args, **kwargs):
        dispatching_value = get_dispatch_value(*args, **kwargs)
        dispatched_to_fn = _multi_inner.__multi__.get(
            dispatching_value,
            _multi_inner.__multi_default__  # Default on missing key
        )
        result = dispatched_to_fn(*args, **kwargs)
        return result

    _multi_inner.__multi__ = {}
    _multi_inner.__multi_default__ \
        = lambda *args, **kwargs: None  # Default default

    return _multi_inner


def multimethod(dispatch_fn=None, dispatch_key=None):
    """Decorates a target function f so that its dispatch table is consulted with
    the given 'dispatch_key' later when f is called. The 'dispatch_fn' must
    be the target of a previous 'multi'. This function adds an entry to the
    empty dispatch table that 'multi' creates.

    Use 'dispatch_key=None' to set a default multimethod for f for cases where
    the name of f has not been bound to a dispatch key.

    The following example illustrates the common case of dispatch-on-type,
    using the types automatically generated by collections.namedtuple, a
    standard type constructor:

    >>> Circle = namedtuple('Circle', ['radius'])
    ...
    ... @multimethod(area_m, Circle)
    ... def area_m(circle):
    ...     return circle.radius ** 2 * PI

    See 'test_locutius.py' for in-depth usage examples.

    """
    def apply_decorator(fn):
        if dispatch_key is None:
            dispatch_fn.__multi_default__ = fn
        else:
            dispatch_fn.__multi__[dispatch_key] = fn
        return dispatch_fn

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
# decoration. See 'test_locutius.py' for in-depth usage examples.


__locutius_multimethods__ = {}


def method(dispatch_value, *args):
    """Returns a new closure, _method_inner, that takes another function -- the
    decorated function -- as argument. The closure _method_inner will be called
    at decoration time with the decorated function as argument.

    The purpose of 'method' is to bind _the name of_ the decorated function to
    a type. We want to end up with multiple particular functions, all with the
    same name, but bound to different types. This is easiest to explain by
    example.

    Let's say we're decorating a particular function named 'area' and binding
    the function to the type 'Circle'. We do this with a definition like the
    following:

    >>> @method(Circle)
    ... def area(circle):
    ...     return circle.radius ** 2 * PI

    'method' is called in the first step of decoration time with argument
    'Circle', which is a type that becomes the 'dispatch value' for this
    particular instance of 'area'. 'method' returns an inner closure over
    dispatch_value. The inner closure, 'method_inner', is now immediately
    called in the second and final step of decoration time with the decorated
    function, 'area', as argument.

    _method_inner first looks up the name 'area' of function 'area' in a global
    __locutius_multimethods__ and doesn't find it (apparently, the Python
    standard 'globals' dictionary does not contain an entry for name 'area',
    using, instead, the name 'fn', which is the name of the function parameter
    to _method_inner). _method_inner will now create and return a
    dispatch function for the pair 'area' and 'Circle' in three steps:

    1. call 'multi' with 'get_dispatch_value' as argument. 'multi' returns an
    inner closure named '_multi_inner'.

      1.a. Because 'method' is only for dispatch-on-type, 'get_dispatch_value'
      is a fixed function that returns the type of its first argument and
      discards the rest of its arguments. Multi closes over
      'get_dispatch_value' inside '_multi_inner', saving it for later use.
      'Get_dispatch_value' will return Circle or Square or Rectangle, etc.,
      depending on how 'area' is called later. 'Multi' sets up an empty
      dispatch table for this closure (instance) of _multi_inner, with a
      harmless default that always returns None. The dispatch table is named
      __multi__.

    2. call 'multimethod' with '_multi_inner' and 'None' as type to set up a
    new, more aggressive default binding for 'area'. This default will be
    called if 'area' is invoked with an instance of a type like 'Blancmange'
    that has no binding for name 'area'. That new default raises a
    'NotImplemented' exception (see 'test_locutius.py' for an example of
    asserting that this exception is raised). 'Multimethod' returns the closure
    '_multi_inner', which closes over the dispatch table.

    3. call 'multimethod' again with '_multi_inner' and 'Circle' to bind the
    original decorated function named 'area' to the type 'Circle'.
    'Multimethod' returns the final, modified (mutated) '_multi_inner';
    'method' returns it immediately so that it replaces the original, decorated
    function named 'area'.

    When the new, decorated 'area' is called with a Circle as argument, as in

    >>> area(Circle(radius=42))

    the mutated _multi_inner is called. It gets the dispatch value (type) by
    calling the previously closed-over 'get_dispatch_value' to get 'Circle'.
    _multi_inner now looks up the key (type) 'Circle' in the dispatch table
    that was previously modified in step 3 above to get the original, decorated
    function named 'area'. _multi_inner finally calls that original, decorated
    function named 'area' with all the args and kwargs that were passed to
    '_multi_inner', and returns the result. The first argument to the original,
    decorated function is the instance of the circle, just as it was to the
    call of 'get_dispatch_value', which used that argument to get the circle's
    type, 'Circle'.

    'multi' and 'multimethod' can be called in other scenarios where the
    dispatch value (lookup key) are not types, but anything desired.

    """

    def get_dispatch_value(t, *args, **kwargs):
        return type(t)

    def not_implemented(*args, **kwargs):
        raise NotImplementedError("Method not implemented for %s" % \
                                  get_dispatch_value(*args, **kwargs))

    def _method_inner(fn):
        # Search for existing multimethod
        nym = fn.__name__
        dispatch_fn = __locutius_multimethods__.get(nym, None)

        if dispatch_fn is None or \
                not hasattr(dispatch_fn, '__multi__'):
            dispatch_fn = multi(get_dispatch_value)
            # call with dispatch_value == None just to set default for d
            dispatch_fn = multimethod(dispatch_fn)(not_implemented)
            __locutius_multimethods__[nym] = dispatch_fn

        return multimethod(dispatch_fn, dispatch_value)(fn)

    return _method_inner
