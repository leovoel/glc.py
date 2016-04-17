"""

    glc.shapes.spiral
    =================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import pi, cos, sin

from .shape import Shape
from ..utils import rad


class Spiral(Shape):

    """Draws a spiral.

    Create it using:

    .. code-block:: python

        render_list.spiral(x=100, y=100, turns=6, inner_radius=10, outer_radius=100)

    Attributes
    ----------
    x : float
        Horizontal position of the spiral.
    y : float
        Vertical position of the spiral.
    inner_radius : float
        Inner radius of the spiral.
    outer_radius : float
        Outer radius of the spiral.
    turns : float
        Number of turns in the spiral (negative values make it turn in the other direction).
    res : float
        The spiral is drawn as a series of tiny line segments.
        This is the angle of each of those segments, in degrees.
    rotation : float
        Angle of the spiral, in degrees).
    scale_x : float
        Horizontal scale factor of the spiral.
    scale_y : float
        Vertical scale factor of the spiral.
    """

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        inner_radius = self.get_number("inner_radius", t, 10)
        outer_radius = self.get_number("outer_radius", t, 90)
        turns = self.get_number("turns", t, 6)
        res = rad(self.get_number("res", t, 1))
        full_angle = pi * 2 * turns
        scale_x = self.get_number("scale_x", t, 1)
        scale_y = self.get_number("scale_y", t, 1)

        context.translate(x, y)
        context.scale(scale_x, scale_y)
        context.rotate(rad(self.get_number("rotation", t, 0)))

        if full_angle > 0:
            a = 0
            while a < full_angle:
                r = inner_radius + (outer_radius - inner_radius) * a / full_angle
                context.line_to(cos(a) * r, sin(a) * r)
                a += res
        else:
            a = full_angle
            while a > 0:
                r = inner_radius + (outer_radius - inner_radius) * a / full_angle
                context.line_to(cos(a) * r, sin(a) * r)
                a -= res

        self.draw_fill_and_stroke(context, t, False, True)
