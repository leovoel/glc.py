"""

    glc.shapes.text
    ===============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from tempfile import TemporaryFile
from .shape import Shape
from ..utils import rad, is_emoji, draw_image

import os
import cairo


class Text(Shape):

    def get_extents(self, context):
        text = self.get_string("text", 0, "Hello world")
        size = self.get_number("size", 0, 20)
        family = self.get_string("family", 0, "sans-serif")
        weight = self.get_string("weight", 0, "normal")

        if weight == "bold":
            _weight = cairo.FONT_WEIGHT_BOLD
        else:
            _weight = cairo.FONT_WEIGHT_NORMAL

        context.save()

        context.select_font_face(family, cairo.FONT_SLANT_NORMAL, _weight)
        context.set_font_size(size)

        ascent, descent, font_height, max_x_advance, max_y_advance = context.font_extents()
        x_bearing, y_bearing, width, height, x_advance, y_advance = context.text_extents(text)

        context.restore()

        extents = {
            "ascent": ascent,
            "descent": descent,
            "font_height": font_height,
            "max_x_advance": max_x_advance,
            "max_y_advance": max_y_advance,
            "x_bearing": x_bearing,
            "y_bearing": y_bearing,
            "text_width": width,
            "text_height": height,
            "x_advance": x_advance,
            "y_advance": y_advance,
        }

        return extents

    def draw(self, context, t):
        x = self.get_number("x", t, 100)
        y = self.get_number("y", t, 100)
        text = self.get_string("text", t, "Hello world")
        size = self.get_number("size", t, 20)
        family = self.get_string("family", t, "sans-serif")
        weight = self.get_string("weight", t, "normal")
        rotation = rad(self.get_number("rotation", t, 0))
        tint = self.get_bool("tint", t, False)

        if weight == "bold":
            _weight = cairo.FONT_WEIGHT_BOLD
        else:
            _weight = cairo.FONT_WEIGHT_NORMAL

        context.select_font_face(family, cairo.FONT_SLANT_NORMAL, _weight)
        context.set_font_size(size)

        fascent, fdescent, fheight, fxadvance, fyadvance = context.font_extents()
        x_off, y_off, tw, th = context.text_extents(text)[:4]
        nx = -tw / 2
        ny = fheight / 2

        context.translate(x, y)
        context.scale(self.get_number("scale_x", t, 1), self.get_number("scale_y", t, 1))
        context.rotate(rotation)

        if self.get_bool("centered", t, True):
            context.translate(nx, ny)

        if self.props.get("emoji_path", False):
            # this is kinda dumb but it's easier
            # than bringing in something like pango
            # (and it wouldn't support emoji image sets anyway)
            for char in text:
                te = context.text_extents(char)

                context.save()

                if is_emoji(char):
                    hex_val = char.encode("unicode-escape").decode("ascii").lstrip("\\U0")

                    if char not in self.props.get("emoji_cache"):
                        # TODO: not assume that .png is the format available
                        path = os.path.abspath(os.path.join(self.props["emoji_path"], hex_val + ".png"))
                        emoji = cairo.ImageSurface.create_from_png(path)
                        self.props.get("emoji_cache")[char] = emoji
                    else:
                        emoji = self.props.get("emoji_cache")[char]

                    if tint:
                        # necessary to prevent reuse
                        f = TemporaryFile()
                        emoji.write_to_png(f)
                        f.seek(0)
                        _emoji = cairo.ImageSurface.create_from_png(f)
                        b = cairo.Context(_emoji)

                        # create alpha mask
                        mask = cairo.ImageSurface(cairo.FORMAT_A8, _emoji.get_width(), _emoji.get_height())
                        maskctx = cairo.Context(mask)
                        maskctx.set_source_surface(_emoji)
                        maskctx.paint()

                        # paint
                        b.set_operator(cairo.OPERATOR_HSL_COLOR)
                        b.set_source_rgba(*self.get_color("fill", t, self.default_styles["fill"]))
                        b.mask(cairo.SurfacePattern(mask))
                    else:
                        _emoji = emoji

                    # scale by the height as that's larger most of the time
                    # if we scaled based on width, the emoji would be too small
                    draw_image(context, _emoji, 0, -fheight * 0.5, te[3], te[3])
                else:
                    context.text_path(char)

                    if self.props.get("stroke_before", False):
                        if self.props.get("stroke", False):
                            context.set_source_rgba(*self.get_color("stroke", t, self.default_styles["stroke"]))
                            context.stroke_preserve()

                        if self.props.get("fill", True):
                            context.set_source_rgba(*self.get_color("fill", t, self.default_styles["fill"]))
                            context.fill_preserve()
                    else:
                        if self.props.get("fill", True):
                            context.set_source_rgba(*self.get_color("fill", t, self.default_styles["fill"]))
                            context.fill_preserve()

                        if self.props.get("stroke", False):
                            context.set_source_rgba(*self.get_color("stroke", t, self.default_styles["stroke"]))
                            context.stroke_preserve()

                context.new_path()
                context.restore()
                context.translate(te[4], te[5])
        else:
            context.text_path(text)
            self.draw_fill_and_stroke(context, t, True, False)
