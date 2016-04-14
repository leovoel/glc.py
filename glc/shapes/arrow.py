"""

    glc.shapes.arrow
    ================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Arrow(Shape):

    """Draws an arrow shape.

    Create it using:

    .. code-block:: python

        render_list.arrow(x=100, y=100, w=100, h=100, point_percent=0.5, shaft_percent=0.5, rotation=0.5)

    Attributes
    ----------
    x : float
        Horizontal position of the center of the arrow.
    y : float
        Vertical position of the center of the arrow.
    w : float
        Width of the arrow.
    h : float
        Height of the arrow.
    point_percent : float
        How much the point of the arrow will take up from the width.
    shaft_percent : float
        How much the shaft of the arrow will take up from the width.
    rotation : float
        Angle of the arrow.
    """

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
