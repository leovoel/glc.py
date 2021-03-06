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

    """Draws a rounded rectangle.

    You can either specify an specific radius for each corner,
    or just an overall radius for all of them.
    
    If a radius for some corner is not specified, it falls back
    to the overall radius.

    Create it using:

    .. code-block:: python

        render_list.round_rect(x=100, y=100, w=100, h=100, radius=10)

    Attributes
    ----------
    x : float
        Horizontal position of the rectangle.
    y : float
        Vertical position of the rectangle.
    w : float
        Width of the rectangle.
    h : float
        Height of the rectangle.
    radius : float
        Overall radius of the corners.
    bottom_left : float
        Radius of the bottom left corner.
    bottom_right : float
        Radius of the bottom right corner.
    top_left : float
        Radius of the bottom left corner.
    top_right : float
        Radius of the bottom right corner.
    rotation : float
        Angle of the rectangle, in degrees.
    centered : bool
        Whether the rectangle should be drawn from the
        center or the top left corner.
        Defaults to ``True``.
    scale_x : float
        Horizontal scale factor of the rectangle.
    scale_y : float
        Vertical scale factor of the rectangle.
    """

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

        context.translate(x, y)

        # put scale here to get isometric effects
        # (probably the only use for these anyway)
        context.scale(self.get_number("scale_x", t, 1), self.get_number("scale_y", t, 1))
        context.rotate(rad(self.get_number("rotation", t, 0)))

        context.save()

        if self.get_bool("centered", t, True):
            context.translate(-w * 0.5, -h * 0.5)

        _r = bottom_right_radius if bottom_right_radius is not None else r

        context.move_to(w, h - _r)
        quadratic_curve_to(context, w, tan(pi / 8) * _r + h - _r, sin(pi / 4) * _r + w - _r, sin(pi / 4) * _r + h - _r)
        quadratic_curve_to(context, tan(pi / 8) * _r + w - _r, h, w - _r, h)

        _r = bottom_left_radius if bottom_left_radius is not None else r

        context.line_to(_r, h)
        quadratic_curve_to(context, -tan(pi / 8) * _r + _r, h, -sin(pi / 4) * _r + _r, sin(pi / 4) * _r + h - _r)
        quadratic_curve_to(context, 0, tan(pi / 8) * _r + h - _r, 0, h - _r)

        _r = top_left_radius if top_left_radius is not None else r

        context.line_to(0, _r)
        quadratic_curve_to(context, 0, -tan(pi / 8) * _r + _r, -sin(pi / 4) * _r + _r, -sin(pi / 4) * _r + _r)
        quadratic_curve_to(context, -tan(pi / 8) * _r + _r, 0, _r, 0)

        _r = top_right_radius if top_right_radius is not None else r

        context.line_to(w - r, 0)
        quadratic_curve_to(context, tan(pi / 8) * _r + w - _r, 0, sin(pi / 4) * _r + w - _r, -sin(pi / 4) * _r + _r)
        quadratic_curve_to(context, w, -tan(pi / 8) * _r + _r, w, _r)

        context.line_to(w, h - (bottom_right_radius if bottom_right_radius is not None else r))

        context.restore()

        self.draw_fill_and_stroke(context, t, False, True)
