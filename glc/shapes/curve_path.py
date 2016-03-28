"""

    glc.shapes.curve_path
    =====================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import quadratic_curve_to


class CurvePath(Shape):

    def draw(self, context, t):
        points = self.get_array("points", t, [])
        loop = self.get_bool("loop", t, False)

        if not points:
            return

        mid_points = []
        i = 0
        while i < len(points) - 1:
            mid_points.append((
                (points[i][0] + points[i + 1][0]) * 0.5,
                (points[i][1] + points[i + 1][1]) * 0.5
            ))
            i += 1

        if loop:
            mid_points.append((
                (points[i][0] + points[0][0]) * 0.5,
                (points[i][1] + points[0][1]) * 0.5
            ))

            context.move_to(mid_points[0][0], mid_points[0][1])

            i = 1
            while i < len(points):
                quadratic_curve_to(context, points[i][0], points[i][1], mid_points[i][0], mid_points[i][1])
                i += 1

            quadratic_curve_to(context, points[0][0], points[0][1], mid_points[0][0], mid_points[0][1])
        else:
            context.move_to(points[0][0], points[0][1])

            i = 1
            while i < len(points) - 2:
                quadratic_curve_to(context, points[i][0], points[i][1], mid_points[i][0], mid_points[i][1])
                i += 1

            quadratic_curve_to(context, points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])

        self.draw_fill_and_stroke(context, t, False, True)
