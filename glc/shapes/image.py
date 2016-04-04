"""

    glc.shapes.image
    ================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from tempfile import TemporaryFile
from .shape import Shape
from ..utils import rad

import cairo


class Image(Shape):

    def draw(self, context, t):
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
        tint = self.get_color("tint", t, None)

        if not img:
            return

        if w is None:
            w = img.get_width()
        if h is None:
            h = img.get_height()

        if tint is not None:
            # necessary to prevent reuse
            f = TemporaryFile()
            img.write_to_png(f)
            f.seek(0)
            _img = cairo.ImageSurface.create_from_png(f)
            b = cairo.Context(_img)

            # create alpha mask
            mask = cairo.ImageSurface(cairo.FORMAT_A8, img.get_width(), img.get_height())
            maskctx = cairo.Context(mask)
            maskctx.set_source_surface(img)
            maskctx.paint()

            # paint
            b.set_operator(cairo.OPERATOR_HSL_COLOR)
            b.set_source_rgba(*tint)
            b.mask(cairo.SurfacePattern(mask))
        else:
            _img = img

        context.save()

        context.translate(x, y)
        context.scale(scale_x, scale_y)
        context.rotate(rotation)

        if self.get_bool("centered", t, True):
            context.translate(-0.5 * w, -0.5 * h)

        context.scale(w / _img.get_width(), h / _img.get_height())

        context.set_source_surface(_img)
        context.paint_with_alpha(alpha)

        context.restore()
