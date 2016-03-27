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
        context.show_text(text)
