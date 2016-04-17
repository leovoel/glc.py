"""

    glc.shapes.curve
    ================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import quadratic_curve_to


class Curve(Shape):

    """Draws a standard quadratic bézier curve using three points.

    Create it using:

    .. code-block:: python

        render_list.curve(x0=20, y0=10, x1=100, y1=200, x2=180, y2=10, show_points=False)

    Attributes
    ----------
    x0 : float
        Horizontal position of the first point.
    y0 : float
        Vertical position of the first point.
    x1 : float
        Horizontal position of the second point.
    y1 : float
        Vertical position of the second point.
    x2 : float
        Horizontal position of the third point.
    y2 : float
        Vertical position of the third point.
    show_points : bool
        Whether to show the points used to draw the curve or not.
        Defaults to ``False``.
    """

    def draw(self, context, t):
        x0 = self.get_number("x0", t, 20)
        y0 = self.get_number("y0", t, 10)
        x1 = self.get_number("x1", t, 100)
        y1 = self.get_number("y1", t, 200)
        x2 = self.get_number("x2", t, 180)
        y2 = self.get_number("y2", t, 10)
        show_points = self.get_bool("show_points", t, False)

        context.move_to(x0, y0)
        quadratic_curve_to(context, x1, y1, x2, y2)

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
