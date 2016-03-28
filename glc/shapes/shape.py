"""

    glc.shapes.shape
    ================

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from ..easing import EASING_FUNCTIONS
from ..value_parser import get_array, get_color, get_bool, get_number, get_string, get_image, get_cairo_constant
from ..utils import randrange

import cairo


class Shape:

    """Represents a drawable shape.

    Do not instantiate this. Use one of its subclasses instead.

    The subclasses should mostly only have to define a ``draw`` method,
    which takes in the context, and t/current time offset.
    """

    def __init__(self, *args, **kwargs):
        self.ease = None
        self.loop = None
        self.props = kwargs
        self.shapes = []

    def add(self, item):
        self.shapes.append(item)
        return item

    def render(self, context, t):
        time = t
        t *= self.props.get("speed_mult", 1)
        t += self.props.get("phase", 0)
        t = self.interpolate(t)

        self.start_draw(context, t)
        self.draw(context, t)
        for shape in self.shapes:
            shape.render(context, time)
        self.end_draw(context, t)

    def interpolate(self, t):
        t %= 1

        if self.loop:
            t = t * 2 if t < 0.5 else (1 - t) * 2

        if callable(self.ease):
            return self.ease(t)

        if self.ease in EASING_FUNCTIONS:
            return EASING_FUNCTIONS[self.ease](t)

        return t

    def start_draw(self, context, t):
        context.save()

        context.set_line_width(self.get_number("line_width", t, self.default_styles["line_width"]))
        context.set_line_cap(self.get_cairo_constant("line_cap", t, self.default_styles["line_cap"]))
        context.set_line_join(self.get_cairo_constant("line_join", t, self.default_styles["line_join"]))
        context.set_miter_limit(self.get_number("miter_limit", t, self.default_styles["miter_limit"]))

        context.translate(
            self.get_number("translation_x", t, self.default_styles["translation_x"]),
            self.get_number("translation_y", t, self.default_styles["translation_y"])
        )

        try:
            shake = self.get_number("shake", t, self.default_styles["shake"])
            context.translate(randrange(-shake, shake), randrange(-shake, shake))
        except ValueError:
            pass

        line_dash = self.get_array("line_dash", t, self.default_styles["line_dash"])
        if line_dash:
            context.set_dash(line_dash)

        context.new_path()

    def draw_fill_and_stroke(self, context, t, do_fill, do_stroke):
        context.save()

        if self.props.get("fill", do_fill):
            context.set_source_rgba(*self.get_color("fill", t, self.default_styles["fill"]))
            context.fill_preserve()

        context.restore()

        if self.props.get("stroke", do_stroke):
            context.set_source_rgba(*self.get_color("stroke", t, self.default_styles["stroke"]))
            context.stroke_preserve()

    def end_draw(self, context, t):
        context.close_path()
        context.restore()

    def get_number(self, prop, t, default):
        return get_number(self.props.get(prop, None), t, default)

    def get_color(self, prop, t, default):
        return get_color(self.props.get(prop, None), t, default)

    def get_string(self, prop, t, default):
        return get_string(self.props.get(prop, None), t, default)

    def get_bool(self, prop, t, default):
        return get_bool(self.props.get(prop, None), t, default)

    def get_array(self, prop, t, default):
        return get_array(self.props.get(prop, None), t, default)

    def get_image(self, prop, t, default):
        return get_image(self.props.get(prop, None), t, default)

    def get_cairo_constant(self, prop, t, default):
        return get_cairo_constant(prop, self.props.get(prop, None), t, default)
