"""

    glc.shapes.poly
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import cos, sin, pi

from .shape import Shape
from ..utils import rad


class Poly(Shape):

    """Draws a polygon.

    Create it using:

    .. code-block:: python

        render_list.poly(x=100, y=100, rotation=0, radius=50, sides=5)

    Attributes
    ----------
    x : float
        Horizontal position of the polygon.
    y : float
        Vertical position of the polygon.
    radius : float
        Radius of the polygon.
    sides : int
        Number of sides of the polygon.
    rotation : float
        Angle of the polygon, in degrees.
    """

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        radius = self.get_number("radius", t, 50)
        rotation = rad(self.get_number("rotation", t, 0))
        sides = int(self.get_number("sides", t, 5))

        context.translate(x, y)
        context.rotate(rotation)
        context.move_to(radius, 0)
        for i in range(1, sides):
            angle = pi * 2 / sides * i
            context.line_to(cos(angle) * radius, sin(angle) * radius)
        context.line_to(radius, 0)

        self.draw_fill_and_stroke(context, t, False, True)
