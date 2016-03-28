"""

    glc.shapes.round_rect
    =====================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import tan, sin, pi

from .shape import Shape
from ..utils import quadratic_curve_to, rad


class RoundRect(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        w = self.get_number("w", t, 100)
        h = self.get_number("h", t, 100)
        r = self.get_number("radius", t, 10)
        bottom_right_radius = self.get_number("bottom_right", t, None)
        bottom_left_radius = self.get_number("bottom_left", t, None)
        top_right_radius = self.get_number("top_right", t, None)
        top_left_radius = self.get_number("top_left", t, None)

        context.save()

        context.translate(x, y)

        # put scale here to get isometric effects
        # (probably the only use for these anyway)
        context.scale(self.get_number("scale_x", t, 1), self.get_number("scale_y", t, 1))
        context.rotate(rad(self.get_number("rotation", t, 0)))

        context.save()

        if self.get_bool("centered", t, True):
            context.translate(-w * 0.5, -h * 0.5)

        _r = bottom_right_radius if bottom_right_radius is not None else r

        context.move_to(x + w, y + h - _r)
        quadratic_curve_to(context, x + w, tan(pi / 8) * _r + y + h - _r, sin(pi / 4) * _r + x + w - _r, sin(pi / 4) * _r + y + h - _r)
        quadratic_curve_to(context, tan(pi / 8) * _r + x + w - _r, y + h, x + w - _r, y + h)

        _r = bottom_left_radius if bottom_left_radius is not None else r

        context.line_to(x + _r, y + h)
        quadratic_curve_to(context, -tan(pi / 8) * _r + x + _r, y + h, -sin(pi / 4) * _r + x + _r, sin(pi / 4) * _r + y + h - _r)
        quadratic_curve_to(context, x, tan(pi / 8) * _r + y + h - _r, x, y + h - _r)

        _r = top_left_radius if top_left_radius is not None else r

        context.line_to(x, y + _r)
        quadratic_curve_to(context, x, -tan(pi / 8) * _r + y + _r, -sin(pi / 4) * _r + x + _r, -sin(pi / 4) * _r + y + _r)
        quadratic_curve_to(context, -tan(pi / 8) * _r + x + _r, y, x + _r, y)

        _r = top_right_radius if top_right_radius is not None else r

        context.line_to(x + w - r, y)
        quadratic_curve_to(context, tan(pi / 8) * _r + x + w - _r, y, sin(pi / 4) * _r + x + w - _r, -sin(pi / 4) * _r + y + _r)
        quadratic_curve_to(context, x + w, -tan(pi / 8) * _r + y + _r, x + w, y + _r)

        context.line_to(x + w, y + h - (bottom_right_radius if bottom_right_radius is not None else r))

        context.restore()

        context.restore()

        self.draw_fill_and_stroke(context, t, False, True)
