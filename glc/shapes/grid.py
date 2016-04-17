"""

    glc.shapes.grid
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape


class Grid(Shape):

    """Draws a grid.

    Create it using:

    .. code-block:: python

        render_list.grid(x=0, y=0, w=100, h=100, size=20)

    Attributes
    ----------
    x : float
        Horizontal position of the grid.
    y : float
        Vertical position of the grid.
    w : float
        Width of the grid.
    h : float
        Height of the grid.
    size : float
        Size of a grid cell.
    """

    def draw(self, context, t):
        x = self.get_number("x", t, 0)
        y = self.get_number("y", t, 0)
        w = self.get_number("w", t, 100)
        h = self.get_number("h", t, 100)
        grid_size = self.get_number("size", t, 20)

        for i in range(y, y + h + 1, grid_size):
            context.move_to(x, i)
            context.line_to(x + w, i)
        for i in range(x, x + w + 1, grid_size):
            context.move_to(i, y)
            context.line_to(i, y + h)

        self.draw_fill_and_stroke(context, t, False, True)
