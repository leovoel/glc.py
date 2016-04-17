"""

    glc.shapes.path
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import floor

from ..utils import clamp
from .shape import Shape


class Path(Shape):

    """Draws lines that pass between the specified points.

    Create it using:

    .. code-block:: python

        render_list.path(path=[0, 0, 100, 100, -100, 100, -50, 50, 0, 50])

    Attributes
    ----------
    path : list of floats
        Flat list of points, like this: `[0, 0, 100, 100]` (two points).
        Can also be a nested list, in which case the points will be interpolated.
        If the two lists are not the same size, excess points will be ignored.
    start_percent : float
        Where drawing of the path will start at.
    end_percent : float
        Where drawing of the path will end at.
    show_points : bool
        Whether to show the points used to draw the path or not.
        Defaults to ``False``.
    """

    def draw(self, context, t):
        path = self.get_array("path", t, [])
        start_percent = self.get_number("start_percent", t, 0)
        end_percent = self.get_number("end_percent", t, 1)
        show_points = self.get_bool("show_points", t, False)

        start_point = floor(len(path) / 2 * start_percent)
        end_point = floor(len(path) / 2 * end_percent)
        start_index = start_point * 2
        end_index = end_point * 2

        if start_index > end_index:
            start_index, end_index = end_index, start_index

        context.move_to(path[start_index], path[clamp(start_index + 1, 0, end_index)])

        for i in range(start_index + 2, end_index - 1, 2):
            context.line_to(path[i], path[i + 1])

        self.draw_fill_and_stroke(context, t, False, True)

        if show_points:
            context.save()
            context.new_path()
            context.set_source_rgb(0, 0, 0)
            for point in path:
                context.rectangle(point[0] - 2, point[1] - 2, 4, 4)
                context.fill()
            context.restore()
