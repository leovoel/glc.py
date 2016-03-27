"""

    glc.shapes.isobox
    =================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape


class IsoBox(Shape):

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        size = self.get_number("size", t, 60)
        h = self.get_number("h", t, 40)
        color_left = self.get_color("color_left", t, 0xff999999)
        color_right = self.get_color("color_right", t, 0xffcccccc)
        color_top = self.get_color("color_top", t, 0xffeeeeee)
        scale_x = self.get_number("scale_x", t, 1)
        scale_y = self.get_number("scale_y", t, 1)

        context.translate(x, y)
        context.scale(scale_x, scale_y)

        if h >= 0:
            context.set_source_rgba(*color_top)
            context.new_path()
            context.move_to(-size / 2, -h)
            context.line_to(0, -size / 4 - h)
            context.line_to(size / 2, -h)
            context.line_to(size / 2, -1)
            context.line_to(0, size / 4 - 1)
            context.line_to(-size / 2, -1)
            context.line_to(-size / 2, -h)
            context.save()
            context.fill_preserve()
            context.restore()

            context.set_source_rgba(*color_left)
            context.new_path()
            context.move_to(-size / 2, 0)
            context.line_to(0, size / 4)
            context.line_to(0, size / 4 - h)
            context.line_to(-size / 2, -h)
            context.line_to(-size / 2, 0)
            context.save()
            context.fill_preserve()
            context.restore()

            context.set_source_rgba(*color_right)
            context.new_path()
            context.move_to(size / 2, 0)
            context.line_to(0, size / 4)
            context.line_to(0, size / 4 - h)
            context.line_to(size / 2, -h)
            context.line_to(size / 2, 0)
            context.save()
            context.fill_preserve()
            context.restore()
        else:
            context.new_path()
            context.move_to(-size / 2, 0)
            context.line_to(0, -size / 4)
            context.line_to(size / 2, 0)
            context.line_to(0, size / 4)
            context.line_to(-size / 2, 0)
            context.clip()

            context.set_source_rgba(*color_right)
            context.new_path()
            context.move_to(-size / 2, 0)
            context.line_to(0, -size / 4)
            context.line_to(0, -size / 4 - h)
            context.line_to(-size / 2, -h)
            context.line_to(-size / 2, 0)
            context.save()
            context.fill_preserve()
            context.restore()

            context.set_source_rgba(*color_left)
            context.new_path()
            context.move_to(size / 2, 0)
            context.line_to(0, -size / 4)
            context.line_to(0, -size / 4 - h)
            context.line_to(size / 2, -h)
            context.line_to(size / 2, 0)
            context.save()
            context.fill_preserve()
            context.restore()

            context.set_source_rgba(*color_top)
            context.new_path()
            context.move_to(-size / 2, -h)
            context.line_to(0, -size / 4 - h)
            context.line_to(size / 2, -h)
            context.line_to(0, size / 4 - h)
            context.line_to(-size / 2, -h)
            context.save()
            context.fill_preserve()
            context.restore()
