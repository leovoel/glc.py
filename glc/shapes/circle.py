"""

    glc.shapes.circle
    =================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Circle(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        radius = self.get_number("radius", t, 50)
        start_angle = self.get_number("start", t, 0)
        end_angle = self.get_number("end", t, 360)
        centered = self.get_bool("centered", t, False)

        context.translate(x, y)
        context.rotate(rad(self.get_number("rotation", t, 0)))
        context.scale(self.get_number("scale_x", t, 1), self.get_number("scale_y", t, 1))

        if centered:
            context.move_to(0, 0)

        context.arc(0, 0, radius, rad(start_angle), rad(end_angle))

        if centered:
            context.close_path()

        self.draw_fill_and_stroke(context, t, True, False)
