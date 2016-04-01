"""

    glc.shapes.text
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad

import cairo


class Text(Shape):

    def get_extents(self, context):
        text = self.get_string("text", 0, "Hello world")
        size = self.get_number("size", 0, 20)
        family = self.get_string("family", 0, "sans-serif")
        weight = self.get_string("weight", 0, "normal")

        if weight == "bold":
            _weight = cairo.FONT_WEIGHT_BOLD
        else:
            _weight = cairo.FONT_WEIGHT_NORMAL

        context.save()

        context.select_font_face(family, cairo.FONT_SLANT_NORMAL, _weight)
        context.set_font_size(size)

        ascent, descent, font_height, max_x_advance, max_y_advance = context.font_extents()
        x_bearing, y_bearing, width, height, x_advance, y_advance = context.text_extents(text)

        context.restore()

        extents = {
            "ascent": ascent,
            "descent": descent,
            "font_height": font_height,
            "max_x_advance": max_x_advance,
            "max_y_advance": max_y_advance,
            "x_bearing": x_bearing,
            "y_bearing": y_bearing,
            "text_width": width,
            "text_height": height,
            "x_advance": x_advance,
            "y_advance": y_advance,
        }

        return extents

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        text = self.get_string("text", t, "Hello world")
        size = self.get_number("size", t, 20)
        family = self.get_string("family", t, "sans-serif")
        weight = self.get_string("weight", t, "normal")
        rotation = rad(self.get_number("rotation", t, 0))

        if weight == "bold":
            _weight = cairo.FONT_WEIGHT_BOLD
        else:
            _weight = cairo.FONT_WEIGHT_NORMAL

        context.select_font_face(family, cairo.FONT_SLANT_NORMAL, _weight)
        context.set_font_size(size)

        fascent, fdescent, fheight, fxadvance, fyadvance = context.font_extents()
        x_off, y_off, tw, th = context.text_extents(text)[:4]
        nx = -tw / 2
        ny = fheight / 2

        context.translate(x, y)
        context.rotate(rotation)
        context.translate(nx, ny)

        if self.get_bool("centered", t, False):
            context.move_to(0, 0)

        context.text_path(text)

        self.draw_fill_and_stroke(context, t, True, False)
