"""

    glc.shapes.curve_segment
    ========================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import quadratic


class CurveSegment(Shape):

    """Draws a portion of a standard quadratic bézier curve using three points.

    The drawn segment will animate from the start of the curve to the
    end of it during the animation (and back to the start if the
    loop attribute on the animation is ``True``).

    Create it using:

    .. code-block:: python

        render_list.curve_segment(x0=20, y0=20, x1=100, y1=200, x2=180, y2=20, percent=0.5, show_points=False)
        # or
        render_list.curveseg(x0=20, y0=20, x1=100, y1=200, x2=180, y2=20, percent=0.5, show_points=False)

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
    percent : float
        How much of the curve should be drawn.
    show_points : bool
        Whether to show the points used to draw the curve or not.
        Defaults to ``False``.
    """

    def draw(self, context, t):
        x0 = self.get_number("x0", t, 20)
        y0 = self.get_number("y0", t, 20)
        x1 = self.get_number("x1", t, 100)
        y1 = self.get_number("y1", t, 200)
        x2 = self.get_number("x2", t, 180)
        y2 = self.get_number("y2", t, 20)
        percent = self.get_number("percent", t, 0.1)
        show_points = self.get_bool("show_points", t, False)

        t1 = t * (1 + percent)
        t0 = t1 - percent
        res = 0.01

        t1 = min(t1, 1.001)
        t0 = max(t0, -0.001)

        i = t0
        while i < t1:
            x = quadratic(i, x0, x1, x2)
            y = quadratic(i, y0, y1, y2)
            if i == t0:
                context.move_to(x, y)
            else:
                context.line_to(x, y)
            i += res

        x = quadratic(t1, x0, x1, x2)
        y = quadratic(t1, y0, y1, y2)
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
            context.restore()
