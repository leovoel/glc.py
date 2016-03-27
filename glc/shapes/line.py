"""

    glc.shapes.line
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape


class Line(Shape):

    def draw(self, context, t):
        x0 = self.get_number("x0", t, 0)
        y0 = self.get_number("y0", t, 0)
        x1 = self.get_number("x1", t, 100)
        y1 = self.get_number("y1", t, 100)

        context.move_to(x0, y0)
        context.line_to(x1, y1)

        self.draw_fill_and_stroke(context, t, False, True)
