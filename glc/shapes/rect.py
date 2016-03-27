"""

    glc.shapes.rect
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Rect(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        w = self.get_number("w", t, 100)
        h = self.get_number("h", t, 100)

        context.save()

        context.translate(x, y)

        # put scale here to get isometric effects
        # (probably the only use for these anyway)
        context.scale(self.get_number("scale_x", t, 1), self.get_number("scale_y", t, 1))
        context.rotate(rad(self.get_number("rotation", t, 0)))

        if self.get_bool("centered", t, True):
            context.rectangle(-w * 0.5, -h * 0.5, w, h)
        else:
            context.rectangle(0, 0, w, h)

        context.restore()

        self.draw_fill_and_stroke(context, t, False, True)
