"""

    glc.shapes.arc_segment
    ======================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class ArcSegment(Shape):

    """This draws an arc around a (x, y) point with a radius and start/end angles,
    but only draws a portion of that arc.

    The drawn segment will animate from the start angle to the end angle
    during the animation (and back to the start angle if the
    loop attribute on the animation is ``True``).

    Create it using:

    .. code-block:: python

        render_list.arc_segment(x=100, y=100, radius=50, start=0, end=360, arc=20, rotation=0)
        # or
        render_list.arcseg(x=100, y=100, radius=50, start=0, end=360, arc=20, rotation=0)

    Attributes
    ----------
    x : float
    y : float
    radius : float
    start : float
    end : float
    arc : float
    rotation : float
    """

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        radius = self.get_number("radius", t, 50)
        start_angle = self.get_number("start", t, 0)
        end_angle = self.get_number("end", t, 360)

        if start_angle > end_angle:
            start_angle, end_angle = end_angle, start_angle

        arc = self.get_number("arc", t, 20)
        start = start_angle - 1
        end = start_angle + t * (end_angle - start_angle + arc)

        if end > start_angle + arc:
            start = end - arc

        if end > end_angle:
            end = end_angle + 1

        context.translate(x, y)
        context.rotate(rad(self.get_number("rotation", t, 0)))
        context.arc(0, 0, radius, rad(start), rad(end))

        self.draw_fill_and_stroke(context, t, False, True)
