"""Adapted from Adam Bard's work at https://unpythonic.com/02_02_multimethods/,
with clarifications, corrections, and unit tests."""

from locutius.multimethods import multi, multimethod, method
from unittest import TestCase
from collections import namedtuple
import pytest


PI = 3.1415926535898


# Named tuples are great for lightweight data modeling, and multimethods close
# the gap between named tuples and classes.


Circle = namedtuple('Circle', ['radius'])
Square = namedtuple('Square', ['side'])
Rectangle = namedtuple('Rectangle', ['width', 'height'])


class Blancmange(object):
    """Establishes a type named 'Blancmange' with no functionality."""
    pass


#  _____ _          _  _             _  __      __
# |_   _| |_  ___  | || |__ _ _ _ __| | \ \    / /_ _ _  _
#   | | | ' \/ -_) | __ / _` | '_/ _` |  \ \/\/ / _` | || |
#   |_| |_||_\___| |_||_\__,_|_| \__,_|   \_/\_/\__,_|\_, |
#                                                     |__/


@multi
def area_m(shape):
    return type(shape)


@multimethod(area_m, Circle)
def area_m(circle):
    return circle.radius ** 2 * PI


@multimethod(area_m, Square)
def area_m(square):
    return square.side ** 2


@multi
def perimeter_m(shape):
    return type(shape)


@multimethod(perimeter_m, Circle)
def perimeter_m(circle):
    return circle.radius * 2 * PI


@multimethod(perimeter_m, Square)
def perimeter_m(square):
    return square.side * 4


class TestRawMultimethods(TestCase):
    def test_area_m_circle(self):
        self.assertEqual(PI, area_m(Circle(radius=1)))

    def test_area_m_square(self):
        self.assertEqual(1, area_m(Square(side=1)))

    def test_area_m_blancmange(self):
        self.assertIs(None, area_m(Blancmange))

    def test_perimeter_m_circle(self):
        self.assertEqual(2 * PI, perimeter_m(Circle(radius=1)))

    def test_perimeter_m_square(self):
        self.assertEqual(4, perimeter_m(Square(side=1)))

    def test_perimeter_m_blancmange(self):
        self.assertIs(None, perimeter_m(Blancmange))


#  _  _      _          _   __  __      _ _   _
# | \| |__ _| |_____ __| | |  \/  |_  _| | |_(_)
# | .` / _` | / / -_) _` | | |\/| | || | |  _| |
# |_|\_\__,_|_\_\___\__,_| |_|  |_|\_,_|_|\__|_|


@multimethod
def no_previous_multi():
    """This is a nonsense definition, but it's not None. It won't be called, as
    we prove by raising an uncaught Exception. It's replaced by a function of
    one argument. That function monkey-patches this function with a default key"""
    raise Exception


def im_not_a_multi():
    """When 'there_is_no_multi_for_this_multimethod' is called, control goes
    here. Test this assertion by checking for 'TypeError' only. 'ValueError'
    will show that this assertion is not true."""
    raise TypeError


@multimethod(im_not_a_multi)
def there_is_no_multi_for_this_multimethod():
    """If 'ValueError' is raised, then we didn't understand the re-plumbing
    that 'multimethod' does in this case. Multimethod should monkey-patch the
    default multimethod to be 'im_not_a_multi'."""
    raise ValueError


with pytest.raises(AttributeError):
    @multimethod(im_not_a_multi, dispatch_key=42)
    def there_isnt_a_multi_here_either():
        """This tries to add a key to a multi dict that doesn't exist."""
        return


def test_cant_have_null_multi():
    assert no_previous_multi is not None
    assert no_previous_multi(42) is not None
    assert there_is_no_multi_for_this_multimethod is not None
    with pytest.raises(TypeError):
        there_is_no_multi_for_this_multimethod()


#  _____ _          ___               __      __
# |_   _| |_  ___  | __|__ _ ____  _  \ \    / /_ _ _  _
#   | | | ' \/ -_) | _|/ _` (_-< || |  \ \/\/ / _` | || |
#   |_| |_||_\___| |___\__,_/__/\_, |   \_/\_/\__,_|\_, |
#                               |__/                |__/


@method(Circle)
def perimeter(circle):
    return circle.radius * 2 * PI


@method(Square)
def perimeter(square):
    return square.side * 4


@method(Rectangle)
def perimeter(rectangle):
    return 2 * (rectangle.width + rectangle.height)


@method(Circle)
def area(circle):
    return circle.radius ** 2 * PI


@method(Square)
def area(square):
    return square.side ** 2


@method(Rectangle)
def area(rectangle):
    return rectangle.width * rectangle.height


class TestProperties(TestCase):

    def setUp(self):
        self.a_circle = Circle(radius=42)
        self.a_square = Square(side=42)
        self.a_rectangle = Rectangle(width=42, height=17)
        self.a_blancmange = Blancmange()

    def test_area_circle(self):
        expected = 42 * 42 * PI
        actual = area(self.a_circle)
        self.assertEqual(expected, actual)

    def test_area_square(self):
        expected = 42 * 42
        actual = area(self.a_square)
        self.assertEqual(expected, actual)

    def test_area_rectangle(self):
        expected = 42 * 17
        actual = area(self.a_rectangle)
        self.assertEqual(expected, actual)

    def test_area_blancmange(self):
        with pytest.raises(NotImplementedError):
            area(self.a_blancmange)

    def test_perimeter_circle(self):
        expected = 2 * 42 * PI
        actual = perimeter(self.a_circle)
        self.assertEqual(expected, actual)

    def test_perimeter_square(self):
        expected = 42 * 4
        actual = perimeter(self.a_square)
        self.assertEqual(expected, actual)

    def test_perimeter_rectangle(self):
        expected = 2 * 42 + 2 * 17
        actual = perimeter(self.a_rectangle)
        self.assertEqual(expected, actual)


#  _  __                       _            _   _    _
# | |/ /___ _  _   ___ ___    /_\  _ _ _  _| |_| |_ (_)_ _  __ _
# | ' </ -_) || | |___|___|  / _ \| ' \ || |  _| ' \| | ' \/ _` |
# |_|\_\___|\_, | |___|___| /_/ \_\_||_\_, |\__|_||_|_|_||_\__, |
#           |__/                       |__/                |___/


# If we didn't know about named tuples, we'd probably do something like this:


circle_d = {'dispatch-key': 'circle', 'radius': 42}
square_d = {'dispatch-key': 'square', 'side': 42}
rectangle_d = {'dispatch-key': 'rectangle', 'width': 42, 'height': 17}
blancmange_d = {'dispatch-key': 'blancmange'}


# We can't use 'method' now; it's only for dispatch-on-type. But we still have
# 'multi' and 'multimethod'.


@multi
def area_d(shape):
    return shape['dispatch-key']


@multimethod(area_d, 'circle')
def area_d(circle):
    return circle['radius'] ** 2 * PI


@multimethod(area_d, 'square')
def area_d(square):
    return square['side'] ** 2


@multimethod(area_d, 'rectangle')
def area_d(rectangle):
    return rectangle['width'] * rectangle['height']


@multi
def perimeter_d(shape):
    return shape['dispatch-key']


@multimethod(perimeter_d, 'circle')
def perimeter_d(circle):
    return circle['radius'] * 2 * PI


@multimethod(perimeter_d, 'square')
def perimeter_d(square):
    return square['side'] * 4


@multimethod(perimeter_d, 'rectangle')
def perimeter_d(rectangle):
    return rectangle['width'] * 2 + rectangle['height'] * 2


class TestArbitraryKeyMultimethods(TestCase):
    def test_area_d_circle(self):
        self.assertEqual(42 * 42 * PI, area_d(circle_d))

    def test_area_d_square(self):
        self.assertEqual(42 * 42, area_d(square_d))

    def test_area_d_rectangle(self):
        self.assertEqual(42 * 17, area_d(rectangle_d))

    def test_area_d_blancmange(self):
        self.assertIs(None, area_d(blancmange_d))

    def test_perimeter_d_circle(self):
        self.assertEqual(2 * 42 * PI, perimeter_d(circle_d))

    def test_perimeter_d_square(self):
        self.assertEqual(42 * 4, perimeter_d(square_d))

    def test_perimeter_d_rectangle(self):
        self.assertEqual(2*(42 + 17), perimeter_d(rectangle_d))

    def test_perimeter_d_blancmange(self):
        self.assertIs(None, perimeter_d(blancmange_d))
