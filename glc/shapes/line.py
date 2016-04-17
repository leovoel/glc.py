"""

    glc.shapes.line
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape


class Line(Shape):

    """Draws a line between two points.

    Create it using:

    .. code-block:: python

        render_list.line(x0=0, y0=0, x1=100, y1=100)

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
    """

    def draw(self, context, t):
        x0 = self.get_number("x0", t, 0)
        y0 = self.get_number("y0", t, 0)
        x1 = self.get_number("x1", t, 100)
        y1 = self.get_number("y1", t, 100)

        context.move_to(x0, y0)
        context.line_to(x1, y1)

        self.draw_fill_and_stroke(context, t, False, True)
