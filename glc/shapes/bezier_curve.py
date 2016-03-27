"""

    glc.shapes.bezier_curve
    =======================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape


class BezierCurve(Shape):

    def draw(self, context, t):
        x0 = self.get_number("x0", t, 50)
        y0 = self.get_number("y0", t, 10)
        x1 = self.get_number("x1", t, 200)
        y1 = self.get_number("y1", t, 100)
        x2 = self.get_number("x2", t, 0)
        y2 = self.get_number("y2", t, 100)
        x3 = self.get_number("x3", t, 150)
        y3 = self.get_number("y3", t, 10)
        show_points = self.get_bool("show_points", t, False)

        context.move_to(x0, y0)
        context.curve_to(x1, y1, x2, y2, x3, y3)

        self.draw_fill_and_stroke(context, t, False, True)

        if show_points:
            context.save()
            context.new_path()
            context.set_source_rgb(0, 0, 0)
            context.rectangle(x0 - 2, y0 - 2, 4, 4)
            context.fill()
            context.rectangle(x1 - 2, y1 - 2, 4, 4)
            context.fill()
            context.rectangle(x2 - 2, y2 - 2, 4, 4)
            context.fill()
            context.rectangle(x3 - 2, y3 - 2, 4, 4)
            context.fill()
            context.restore()
