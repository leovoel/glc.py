"""

    glc.shapes.oval
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Oval(Shape):

    """Draws an oval.

    This can also draw an ovoidal arc, if you use the start and end angle properties to do so.

    Create it using:

    .. code-block:: python

        render_list.oval(x=100, y=100, rx=100, ry=50)

    Attributes
    ----------
    x : float
        Horizontal position of the oval.
    y : float
        Vertical position of the oval.
    rx : float
        Horizontal radius of the oval.
    ry : float
        Vertical radius of the oval.
    start : float
        Start angle of the arc, in degrees.
    end : float
        End angle of the arc, in degrees.
    centered : bool
        Whether the oval should be centered on the (x, y)
        point or not. Defaults to ``False``.
    rotation : float
        Angle of the oval, in degrees.
    """

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        rx = self.get_number("rx", t, 50)
        ry = self.get_number("ry", t, 50)
        start_angle = self.get_number("start", t, 0)
        end_angle = self.get_number("end", t, 360)
        draw_from_center = self.get_bool("centered", t, False)

        context.translate(x, y)
        context.rotate(rad(self.get_number("rotation", t, 0)))
        context.save()
        context.scale(rx * 0.01, ry * 0.01)

        if draw_from_center:
            context.moveTo(0, 0)

        context.arc(0, 0, 100, rad(start_angle), rad(end_angle))

        if draw_from_center:
            context.closePath()
        context.restore()

        self.draw_fill_and_stroke(context, t, True, False)
