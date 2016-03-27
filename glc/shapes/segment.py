"""

    glc.shapes.segment
    ==================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import atan2, hypot

from .shape import Shape


class Segment(Shape):

    def draw(self, context, t):
        x0 = self.get_number("x0", t, 0)
        y0 = self.get_number("y0", t, 0)
        x1 = self.get_number("x1", t, 100)
        y1 = self.get_number("y1", t, 100)
        segment_length = self.get_number("length", t, 50)
        dx = x1 - x0
        dy = y1 - y0
        angle = atan2(dy, dx)
        dist = hypot(dx, dy)
        start = -0.01
        end = (dist + segment_length) * t

        if end > segment_length:
            start = end - segment_length

        if end > dist:
            end = dist + 0.01

        context.translate(x0, y0)
        context.rotate(angle)
        context.move_to(start, 0)
        context.line_to(end, 0)

        self.draw_fill_and_stroke(context, t, False, True)
