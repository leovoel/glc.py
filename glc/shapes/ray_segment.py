"""

    glc.shapes.ray_segment
    ======================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class RaySegment(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        angle = rad(self.get_number("angle", t, 0))
        length = self.get_number("length", t, 100)
        segment_length = self.get_number("segment_length", t, 50)
        start = -0.01
        end = (length + segment_length) * t

        if end > segment_length:
            start = end - segment_length

        if end > length:
            end = length + 0.01

        context.translate(x, y)
        context.rotate(angle)
        context.move_to(start, 0)
        context.line_to(length, 0)

        self.draw_fill_and_stroke(context, t, False, True)
