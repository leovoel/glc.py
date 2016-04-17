"""

    glc.shapes.bezier_segment
    =========================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import bezier


class BezierSegment(Shape):

    """Draws a portion of a standard bézier curve using four points.

    The drawn segment will animate from the start of the curve to the
    end of it during the animation (and back to the start if the
    loop attribute on the animation is ``True``).

    Create it using:

    .. code-block:: python

        render_list.bezier_segment(x0=50, y0=10, x1=200, y1=100, x2=0, y2=100, x3=150, y3=10, percent=0.5, show_points=False)
        # or
        render_list.bezierseg(x0=50, y0=10, x1=200, y1=100, x2=0, y2=100, x3=150, y3=10, percent=0.5, show_points=False)

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
    x3 : float
        Horizontal position of the fourth point.
    y3 : float
        Vertical position of the fourth point.
    percent : float
        How much of the bézier curve should be drawn.
    show_points : bool
        Whether to show the points used to draw the curve or not.
        Defaults to ``False``.
    """

    def draw(self, context, t):
        x0 = self.get_number("x0", t, 50)
        y0 = self.get_number("y0", t, 10)
        x1 = self.get_number("x1", t, 200)
        y1 = self.get_number("y1", t, 100)
        x2 = self.get_number("x2", t, 0)
        y2 = self.get_number("y2", t, 100)
        x3 = self.get_number("x3", t, 150)
        y3 = self.get_number("y3", t, 10)
        percent = self.get_number("percent", t, 0.1)
        show_points = self.get_bool("show_points", t, False)

        t1 = t * (1 + percent)
        t0 = t1 - percent
        res = 0.01

        t1 = min(t1, 1.001)
        t0 = max(t0, -0.001)

        i = t0
        while i < t1:
            x = bezier(i, x0, x1, x2, x3)
            y = bezier(i, y0, y1, y2, y3)
            if i == t0:
                context.move_to(x, y)
            else:
                context.line_to(x, y)
            i += res

        x = bezier(t1, x0, x1, x2, x3)
        y = bezier(t1, y0, y1, y2, y3)
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
            context.rectangle(x3 - 2, y3 - 2, 4, 4)
            context.fill()
            context.restore()
