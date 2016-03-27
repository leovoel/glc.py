"""

    glc.shapes.gradient_pie
    =======================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import pi, cos, sin

from .shape import Shape
from ..utils import rad, remap
from ..color import hsva


class GradientPie(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        rx = self.get_number("rx", t, 100)
        ry = self.get_number("ry", t, 100)
        rotation = rad(self.get_number("rotation", t, 0))

        _res = 100
        _default_colors = [hsva(remap(i, 0, _res, 0, 360), 1, 1) for i in range(_res)]

        colors = self.get_array("colors", t, _default_colors)

        length = len(colors)
        start = rotation * 2 * pi
        step = (2 * pi) / length
        ox = cos(start) * rx
        oy = sin(start) * ry

        context.translate(x, y)

        for i in range(length):
            current_angle = start + step * (i + 1)
            cx = cos(current_angle) * rx
            cy = sin(current_angle) * ry

            context.set_source_rgba(*colors[i])

            context.move_to(ox, oy)
            context.line_to(0, 0)
            context.line_to(cx, cy)
            context.line_to(ox, oy)

            context.fill_preserve()

            context.set_line_width(1)
            context.stroke()

            ox = cx
            oy = cy
