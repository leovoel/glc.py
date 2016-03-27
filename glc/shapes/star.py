"""

    glc.shapes.star
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import pi, cos, sin

from .shape import Shape
from ..utils import rad


class Star(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        inner_radius = self.get_number("inner_radius", t, 25)
        outer_radius = self.get_number("outer_radius", t, 50)
        rotation = rad(self.get_number("rotation", t, 0))
        points = self.get_number("points", t, 5)
        scale_x = self.get_number("scale_x", t, 1)
        scale_y = self.get_number("scale_y", t, 1)

        context.translate(x, y)
        context.scale(scale_x, scale_y)
        context.rotate(rotation)
        context.move_to(outer_radius, 0)

        for i in range(1, points * 2):
            angle = pi * 2 / points / 2 * i
            r = inner_radius if i % 2 else outer_radius
            context.line_to(cos(angle) * r, sin(angle) * r)

        context.close_path()

        self.draw_fill_and_stroke(context, t, True, False)
