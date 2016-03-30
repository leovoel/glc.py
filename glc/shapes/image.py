"""

    glc.shapes.image
    ================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .shape import Shape
from ..utils import rad


class Image(Shape):

    def draw(self, context, t):
        # TODO: implement tinting?

        mode = self.get_string("mode", t, "clamp")
        img_ease = self.get_bool("img_ease", t, True)
        img_speed = self.get_number("img_speed", t, 1)

        if img_ease:
            img = self.get_image("image_surfaces", self.interpolate(self.no_interp_time * img_speed), None, mode)
        else:
            img = self.get_image("image_surfaces", self.no_interp_time * img_speed, None, mode)

        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        w = self.get_number("w", t, None)
        h = self.get_number("h", t, None)
        scale_x = self.get_number("scale_x", t, 1)
        scale_y = self.get_number("scale_y", t, 1)
        alpha = self.get_number("alpha", t, 1)
        rotation = rad(self.get_number("rotation", t, 0))

        if not img:
            return

        if w is None:
            w = img.get_width()
        if h is None:
            h = img.get_height()

        context.save()

        context.translate(x, y)
        context.scale(scale_x, scale_y)
        context.rotate(rotation)

        if self.get_bool("centered", t, True):
            context.translate(-0.5 * w, -0.5 * h)

        context.scale(w / img.get_width(), h / img.get_height())

        context.set_source_surface(img)
        context.paint_with_alpha(alpha)

        context.restore()
