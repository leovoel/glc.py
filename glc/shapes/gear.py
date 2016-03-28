"""

    glc.shapes.gear
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import pi

from .shape import Shape
from ..utils import rad


class Gear(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        radius = self.get_number("radius", t, 50)
        tooth_height = self.get_number("tooth_height", t, 10)
        hub = self.get_number("hub", t, 10)
        rotation = rad(self.get_number("rotation", t, 0))
        teeth = int(self.get_number("teeth", t, 10))
        tooth_angle = self.get_number("tooth_angle", t, 0.3)
        face = 0.5 - tooth_angle / 2
        side = 0.5 - face
        inner_radius = radius - tooth_height
        scale_x = self.get_number("scale_x", t, 1)
        scale_y = self.get_number("scale_y", t, 1)

        context.translate(x, y)
        context.scale(scale_x, scale_y)
        context.rotate(rotation)
        context.save()
        context.move_to(radius, 0)
        angle = pi * 2 / teeth

        for i in range(teeth):
            context.rotate(angle * face)
            context.line_to(radius, 0)
            context.rotate(angle * side)
            context.line_to(inner_radius, 0)
            context.rotate(angle * face)
            context.line_to(inner_radius, 0)
            context.rotate(angle * side)
            context.line_to(radius, 0)

        context.line_to(radius, 0)
        context.restore()

        context.move_to(hub, 0)
        context.arc(0, 0, hub, 0, pi * 2)

        self.draw_fill_and_stroke(context, t, True, False)
