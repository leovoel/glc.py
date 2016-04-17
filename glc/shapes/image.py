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

    """Draws an image.

    This uses the `imageio`_ library for loading images.
    See their `docs`_ for more info on what you can load.

    .. _imageio: https://github.com/imageio/imageio
    .. _docs: http://imageio.readthedocs.org/en/latest/userapi.html#imageio.get_reader

    Create it using:

    .. code-block:: python

        render_list.image(img="path/to/image.png", x=100, y=100)
        # or
        render_list.img(img="path/to/image.png", x=100, y=100)

        # you can pass an emoji character as the path
        # which will load an emoji from your emoji_path
        render_list.img(img="\N{OK HAND SIGN}", x=100, y=100)

        # you can pass a list of images
        render_list.img(img=["1.png", "2.png", "3.png"], x=100, y=100)

        # or a gif
        render_list.img(img="numbers.gif", x=100, y=100)

        # you can tint the image
        render_list.img(img="image.png", x=100, y=100, tint=glc.Color("0xffff0000"))

        # you can also control whether the image swapping should be eased
        # of course this only has any effect if it's a multi-image container, such as gifs
        render_list.img(img="image.gif", x=100, y=100, img_ease=False)
        render_list.img(img="image.gif", x=100, y=100, img_ease=False, img_speed=2)

        # the mode attribute controls how wrapping around happens
        # clamp stops at the final frame
        # wrap moves back to the first frame
        render_list.img(img="image.gif", x=100, y=100, img_ease=False, mode="clamp")
        render_list.img(img="image.gif", x=100, y=100, img_ease=False, mode="wrap")

    Attributes
    ----------
    img
        The image or images to use.
        Can be a file path, http address, file object, raw bytes,
        emoji (unicode codepoint), or a list with any of those.
    x : float
        Horizontal position of the image.
    y : float
        Vertical position of the image.
    w : float
        Width of the image. If no value is specified,
        the original image width is used.
    h : float
        Height of the image. If no value is specified,
        the original image height is used.
    scale_x : float
        Horizontal scale factor of the image.
    scale_y : float
        Vertical scale factor of the image.
    centered : bool
        Whether the image should be drawn with (x, y)
        being at its center or at the top-left corner.
        Defaults to ``True``.
    rotation : float
        Angle of the image, in degrees.
    alpha : float
        Opacity of the image.
    tint : :class:`glc.Color`
        Color to tint the image with.
    mode : string
        The image swapping wrapping mode.
        Can only be of the following:

        - clamp
        - wrap

    img_ease : bool
        Whether the image swapping should be eased
        with the rest of the animation or not.
        Defaults to ``True``.
    img_speed : float
        Image swapping speed multiplier.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = kwargs.pop("duration", None)
        self.frame_durations = kwargs.pop("durations", None)

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
