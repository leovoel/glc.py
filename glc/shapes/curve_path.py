"""

    glc.shapes.curve_path
    =====================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import curve_path


class CurvePath(Shape):

    def draw(self, context, t):
        points = self.get_point_array("points", t, [])
        loop = self.get_bool("loop", t, False)

        if not points:
            return

        curve_path(context, points, loop)

        self.draw_fill_and_stroke(context, t, False, True)
