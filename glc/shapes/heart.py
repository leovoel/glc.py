"""

    glc.shapes.heart
    ================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Heart(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        w = self.get_number("w", t, 50)
        h = self.get_number("h", t, 50)
        scale_x = self.get_number("scale_x", t, 1)
        scale_y = self.get_number("scale_y", t, 1)

        x0 = 0
        y0 = -0.25
        x1 = 0.2
        y1 = -0.8
        x2 = 1.1
        y2 = -0.2
        x3 = 0
        y3 = 0.5

        context.save()

        context.translate(x, y)
        context.scale(scale_x, scale_y)
        context.rotate(rad(self.get_number("rotation", t, 0)))

        context.save()

        context.scale(w, h)
        context.move_to(x0, y0)
        context.curve_to(x1, y1, x2, y2, x3, y3)
        context.curve_to(-x2, y2, -x1, y1, -x0, y0)

        context.restore()

        self.draw_fill_and_stroke(context, t, True, False)

        context.restore()
