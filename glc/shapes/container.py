"""

    glc.shapes.container
    ====================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Container(Shape):

    def draw(self, context, t):
        context.translate(self.get_number("x", t, 0), self.get_number("y", t, 0))
        context.rotate(rad(self.get_number("rotation", t, 0)))
        context.scale(self.get_number("scale_x", t, 1), self.get_number("scale_y", t, 1))
