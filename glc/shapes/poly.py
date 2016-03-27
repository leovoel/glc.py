"""

    glc.shapes.poly
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import cos, sin, pi

from .shape import Shape
from ..utils import rad


class Poly(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        radius = self.get_number("radius", t, 50)
        rotation = rad(self.get_number("rotation", t, 0))
        sides = self.get_number("sides", t, 5)

        context.translate(x, y)
        context.rotate(rotation)
        context.move_to(radius, 0)
        for i in range(1, sides):
            angle = pi * 2 / sides * i
            context.line_to(cos(angle) * radius, sin(angle) * radius)
        context.line_to(radius, 0)

        self.draw_fill_and_stroke(context, t, False, True)
