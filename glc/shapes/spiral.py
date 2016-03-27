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
