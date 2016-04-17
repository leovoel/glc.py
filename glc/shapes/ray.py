"""

    glc.shapes.ray
    ==============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Ray(Shape):

    """Draws a ray.

    This does the same thing as :class:`glc.shapes.Line`, but the
    line is specified using a starting point and an angle + length,
    and not explicit points.

    Create it using:

    .. code-block:: python

        render_list.ray(x=100, y=100, angle=0, length=100)

    Attributes
    ----------
    x : float
        Horizontal position of the ray.
    y : float
        Vertical position of the ray.
    angle : float
        Angle of the ray, in degrees.
    length : float
        Length of the ray.
    """

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        angle = rad(self.get_number("angle", t, 0))
        length = self.get_number("length", t, 100)

        context.translate(x, y)
        context.rotate(angle)
        context.move_to(0, 0)
        context.line_to(length, 0)

        self.draw_fill_and_stroke(context, t, False, True)
