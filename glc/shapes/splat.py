"""

    glc.shapes.splat
    =====================

    Based on https://github.com/bit101/shapes/blob/master/shapes.js#L282

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import pi, sin, cos
from random import random

from .shape import Shape
from ..utils import curve_path, rad


class Splat(Shape):

    def make_point(self, angle, radius):
        return (cos(angle) * radius, sin(angle) * radius)

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        num_nodes = self.get_number("num_nodes", t, 5)
        radius = self.get_number("radius", t, 50)
        inner_radius = self.get_number("inner_radius", t, 20)
        curve = self.get_number("curve", t, 0)
        variation = self.get_number("variation", t, 0)
        rotation = rad(self.get_number("rotation", t, 0))

        points = []
        slice_ = pi * 2 / (num_nodes * 2)
        angle = 0
        radius_range = radius - inner_radius

        for i in range(num_nodes):
            r = radius + variation * (random() * radius_range * 2 - radius_range)
            points.append(self.make_point(angle - slice_ * (1 + curve), inner_radius))
            points.append(self.make_point(angle + slice_ * curve, inner_radius))
            points.append(self.make_point(angle - slice_ * curve, r))
            points.append(self.make_point(angle + slice_ * (1 + curve), r))
            angle += slice_ * 2

        context.save()
        context.translate(x, y)
        context.rotate(rotation)
        curve_path(context, points, True)
        context.restore()

        self.draw_fill_and_stroke(context, t, False, True)
