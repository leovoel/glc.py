"""

    glc.shapes.isotube
    ==================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import pi

from .shape import Shape

import cairo


class IsoTube(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        radius = self.get_number("radius", t, 60)
        h = self.get_number("h", t, 40)
        color_left = self.get_color("color_left", t, 0xff999999)
        color_right = self.get_color("color_right", t, 0xffcccccc)
        color_top = self.get_color("color_top", t, 0xffeeeeee)
        scale_x = self.get_number("scale_x", t, 1)
        scale_y = self.get_number("scale_y", t, 1)

        context.translate(x, y)
        context.scale(scale_x, scale_y)

        gradient = cairo.LinearGradient(-radius, 0, radius, 0)

        if h >= 0:
            gradient.add_color_stop_rgba(0, *color_left)
            gradient.add_color_stop_rgba(1, *color_right)
            context.set_source(gradient)
            context.save()
            context.scale(1, 0.5)
            context.new_path()
            context.arc(0, 0, radius, 0, pi * 2)
            context.fill()
            context.restore()

            context.rectangle(-radius, -h, radius * 2, h)
            context.fill()

            context.set_source_rgba(*color_top)
            context.save()
            context.translate(0, -h)
            context.scale(1, 0.5)
            context.new_path()
            context.arc(0, 0, radius, 0, pi * 2)
            context.fill()
            context.restore()
        else:
            gradient.add_color_stop_rgba(1, *color_left)
            gradient.add_color_stop_rgba(0 , *color_right)

            context.save()
            context.scale(1, 0.5)
            context.new_path()
            context.arc(0, 0, radius, 0, pi * 2)
            context.restore()
            context.clip()

            context.set_source(gradient)
            context.rectangle(-radius, -radius / 2, radius * 2, radius * 2)
            context.fill()

            context.save()
            context.translate(0, -h)
            context.scale(1, 0.5)
            context.set_source_rgba(*color_top)
            context.new_path()
            context.arc(0, 0, radius, 0, pi * 2)
            context.fill()
            context.restore()
