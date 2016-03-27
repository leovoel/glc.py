"""

    glc.shapes.curve_segment
    ========================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import quadratic


class CurveSegment(Shape):

    def draw(self, context, t):
        x0 = self.get_number("x0", t, 20)
        y0 = self.get_number("y0", t, 20)
        x1 = self.get_number("x1", t, 100)
        y1 = self.get_number("y1", t, 200)
        x2 = self.get_number("x2", t, 180)
        y2 = self.get_number("y2", t, 20)
        percent = self.get_number("percent", t, 0.1)
        show_points = self.get_bool("show_points", t, False)

        t1 = t * (1 + percent)
        t0 = t1 - percent
        res = 0.01

        t1 = min(t1, 1.001)
        t0 = max(t0, -0.001)

        i = t0
        while i < t1:
            x = quadratic(i, x0, x1, x2)
            y = quadratic(i, y0, y1, y2)
            if i == t0:
                context.move_to(x, y)
            else:
                context.line_to(x, y)
            i += res

        x = quadratic(t1, x0, x1, x2)
        y = quadratic(t1, y0, y1, y2)
        context.line_to(x, y)

        self.draw_fill_and_stroke(context, t, False, True)

        if show_points:
            context.save()
            context.new_path()
            context.set_source_rgb(0, 0, 0)
            context.rectangle(x0 - 2, y0 - 2, 4, 4)
            context.fill()
            context.rectangle(x1 - 2, y1 - 2, 4, 4)
            context.fill()
            context.rectangle(x2 - 2, y2 - 2, 4, 4)
            context.fill()
            context.restore()
