"""

    glc.shapes.arrow
    ================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Arrow(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        w = self.get_number("w", t, 100)
        h = self.get_number("h", t, 100)
        point_percent = self.get_number("point_percent", t, 0.5)
        shaft_percent = self.get_number("shaft_percent", t, 0.5)

        context.translate(x, y)
        context.rotate(rad(self.get_number("rotation", t, 0)))

        context.translate(-w / 2, 0)

        context.move_to(0, -h * shaft_percent * 0.5)
        context.line_to(w - w * point_percent, -h * shaft_percent * 0.5)
        context.line_to(w - w * point_percent, -h * 0.5)
        context.line_to(w, 0)
        context.line_to(w - w * point_percent, h * 0.5)
        context.line_to(w - w * point_percent, h * shaft_percent * 0.5)
        context.line_to(0, h * shaft_percent * 0.5)
        context.line_to(0, -h * shaft_percent * 0.5)

        self.draw_fill_and_stroke(context, t, True, False)
