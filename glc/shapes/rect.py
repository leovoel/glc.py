"""

    glc.shapes.rect
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Rect(Shape):

    """Draws a rectangle.

    Create it using:

    .. code-block:: python

        render_list.rect(x=100, y=100, w=100, h=100)

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

        context.translate(x, y)

        # put scale here to get isometric effects
        # (probably the only use for these anyway)
        context.scale(self.get_number("scale_x", t, 1), self.get_number("scale_y", t, 1))
        context.rotate(rad(self.get_number("rotation", t, 0)))

        if self.get_bool("centered", t, True):
            context.rectangle(-w * 0.5, -h * 0.5, w, h)
        else:
            context.rectangle(0, 0, w, h)

        self.draw_fill_and_stroke(context, t, False, True)
