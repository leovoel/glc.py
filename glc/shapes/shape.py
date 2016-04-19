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

    A lot of the properties passed in can be lists/tuples with two or
    more values, which will animate from one to the other. Depending
    on the amount of values (and the property itself) there will
    be no interpolation, just immediate change from one value to another.

    They can also be callables, which should take in a time ``t`` and return
    a single value of the type it expects; so a :class:`Color` for fills, etc.

    The properties listed here are common to all shapes, but
    some do not work, as it wouldn't make much sense.

    Attributes
    ----------
    speed_mult : float
        Multiplier for the time ``t`` applied to this shape.
    phase : float
        The "local offset" for the time ``t`` applied to this shape.
    translation_x : float
        The horizontal offset for the position of the shape.
    translation_y : float
        The vertical offset for the position of the shape.
    line_width : float
        The width of the outlines for the shape.
    line_cap : int
    line_join : int
    line_dash : iterable of floats
    miter_limit : float
    shake : float
        How much the shape should shake.
    fill : :class:`Color`
        Color the fill of this shape. Can also be a value like ``None`` or ``False``
        to indicate that no filling should be done.
    stroke : :class:`Color`
        Color the outline of this shape. Can also be a value like ``None`` or ``False``
        to indicate that no stroking should be done.
    ease : callable or string
        Either a string, which denotes which easing function to pick from the defaults,
        or a callable, which should take in a time ``t`` and return a single value.
        By default it inherits this attribute from the :class:`Animation` that contains it.
    loop : bool
        Whether this shape should bounce back to its initial properties.
        By default it inherits this attribute from the :class:`Animation` that contains it.
    parent : :class:`Shape`
        Specifies the parent for this shape. The position of it becomes relative to its
        parent, as is the rotation.
        Usually is ``None``.
    """

    def __init__(self, *args, **kwargs):
        self.ease = None
        self.loop = None
        self.props = kwargs
        self.shapes = []

    def add(self, item):
        """Adds a child shape to this shape's list of children.

        Shouldn't be called normally, as this is called automatically
        when you set a shape as a parent of another, for example:

        .. code-block:: python

            circle_a = render_list.circle(x=100, y=100, radius=50)
            render_list.circle(x=100, y=0, radius=50, parent=circle_a)

        Parameters
        ----------
        item : :class:`Shape`
            The shape to add as a child of this one.

        Returns
        -------
        item : :class:`Shape`
            The added child.
        """
        self.shapes.append(item)
        return item

    def set_prop(self, **kwargs):
        """Sets properties for this shape.

        Returns
        -------
        self : :class:`Shape`
            For method chaining.
        """
        self.props.update(kwargs)
        return self

    def set_ease(self, ease="sine"):
        """Sets the easing function for this shape.

        Parameters
        ----------
        ease : callable or str
            Either a string, which denotes which easing function to pick from the defaults,
            or a callable, which should take in a time ``t`` and return a single value.
            Defaults to ``"sine"``.

        Returns
        -------
        self : :class:`Shape`
            For method chaining.
        """
        self.ease = ease
        return self

    def set_loop(self, loop=True):
        """Sets whether this shape should loop or not.

        Parameters
        ----------
        loop : bool
            Whether this shape should bounce back to its initial properties.
            Defaults to ``True``.

        Returns
        -------
        self : :class:`Shape`
            For method chaining.
        """
        self.loop = loop
        return self

    def render(self, context, t):
        time = t
        t *= self.props.get("speed_mult", 1)
        t += self.props.get("phase", 0)
        self.no_interp_time = t
        t = self.interpolate(t)

        self.start_draw(context, t)
        self.draw(context, t)
        for shape in self.shapes:
            shape.render(context, time)
        self.end_draw(context, t)

    def interpolate(self, t, wrap=True):
        if wrap:
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
        context.set_line_cap(self.get_cairo_constant("line_cap", "line_cap", t, self.default_styles["line_cap"]))
        context.set_line_join(self.get_cairo_constant("line_join", "line_join", t, self.default_styles["line_join"]))
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

        if self.props.get("stroke_before", False):
            if self.props.get("stroke", do_stroke):
                context.set_source_rgba(*self.get_color("stroke", t, self.default_styles["stroke"]))
                context.stroke_preserve()

            if self.props.get("fill", do_fill):
                context.set_source_rgba(*self.get_color("fill", t, self.default_styles["fill"]))
                context.fill_preserve()
        else:
            if self.props.get("fill", do_fill):
                context.set_source_rgba(*self.get_color("fill", t, self.default_styles["fill"]))
                context.fill_preserve()

            if self.props.get("stroke", do_stroke):
                context.set_source_rgba(*self.get_color("stroke", t, self.default_styles["stroke"]))
                context.stroke_preserve()

        context.restore()


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

    def get_image(self, prop, t, default, wrap):
        return get_image(self.props.get(prop, None), t, default, wrap)

    def get_cairo_constant(self, name, prop, t, default):
        return get_cairo_constant(name, self.props.get(prop, None), t, default)
