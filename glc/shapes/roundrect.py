"""

    glc.shapes.round_rect
    =====================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import arc_to, rad


class RoundRect(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        w = self.get_number("w", t, 100)
        h = self.get_number("h", t, 100)
        r = self.get_number("radius", t, 10)

        context.save()

        context.translate(x, y)

        # put scale here to get isometric effects
        # (probably the only use for these anyway)
        context.scale(self.get_number("scale_x", t, 1), self.get_number("scale_y", t, 1))
        context.rotate(rad(self.get_number("rotation", t, 0)))

        context.save()

        if self.get_bool("centered", t, True):
            context.translate(-w * 0.5, -h * 0.5)

        context.move_to(r, 0)
        context.line_to(w - r, 0)
        arc_to(context, w, 0, w, r, r)
        context.line_to(w, h - r)
        arc_to(context, w, h, w - r, h, r)
        context.line_to(r, h)
        arc_to(context, 0, h, 0, h - r, r)
        context.line_to(0, r)
        arc_to(context, 0, 0, r, 0, r)

        context.restore()

        context.restore()

        self.draw_fill_and_stroke(context, t, False, True)
