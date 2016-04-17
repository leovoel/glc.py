"""

    glc.shapes.container
    ====================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Container(Shape):

    """This is an empty shape, meant to have shapes added to.

    The container can be rotated, translated and scaled,
    with all of its children being affected.

    Create it using:

    .. code-block:: python

        my_container = render_list.container(x=100, y=100, rotation=45, scale_x=2, scale_y=1)
        # then add shapes to it
        render_list.circle(x=0, y=0, radius=100, parent=my_container)
        render_list.rect(x=0, y=0, w=50, h=50, parent=my_container)

    Attributes
    ----------
    x : float
        Horizontal position of the container.
    y : float
        Vertical position of the container.
    rotation : float
        Angle of the container, in degrees.
    scale_x : float
        Horizontal scale factor of the container.
    scale_y : float
        Vertical scale factor of the container.
    """

    def draw(self, context, t):
        context.translate(self.get_number("x", t, 0), self.get_number("y", t, 0))
        context.rotate(rad(self.get_number("rotation", t, 0)))
        context.scale(self.get_number("scale_x", t, 1), self.get_number("scale_y", t, 1))
