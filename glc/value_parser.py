"""

    glc.value_parser
    ================

    Parsing possible values for shape properties.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from numbers import Number
from math import floor
from .utils import lerp, clamp, quadratic, bezier
from .color import Color, str2color, clerp, multi_clerp

import cairo


# TODO: make these parsers more robust.


def is_arr(item):
    return isinstance(item, (tuple, list))


def pick_from_array(prop, t, interpolate=True):
    if interpolate:
        if len(prop) == 2:
            return lerp(t, prop[0], prop[1])
        if len(prop) == 3:
            return quadratic(t, prop[0], prop[1], prop[2])
        elif len(prop) == 4:
            return bezier(t, prop[0], prop[1], prop[2], prop[3])
    return prop[clamp(floor(t * len(prop)), 0, len(prop) - 1)]


def get_number(prop, t, default):
    if prop is None:
        return default

    out = None

    if isinstance(prop, Number):
        out = prop
    elif callable(prop):
        out = prop(t)
    elif is_arr(prop):
        out = pick_from_array(prop, t)
    elif isinstance(prop, str):
        # yolo
        try:
            out = int(prop)
        except Exception:
            out = float(prop)

    return out


def get_string(prop, t, default):
    if prop is None:
        return default

    out = None

    if isinstance(prop, str):
        out = prop
    elif callable(prop):
        out = prop(t)
    elif is_arr(prop):
        out = pick_from_array(prop, t, False)

    return out


TRUE_VALUES = ("on", "yes", "true", "1", "enable", "confirm", "y", "t")
FALSE_VALUES = ("off", "no", "false", "0", "disable", "cancel", "n", "f")


def str2bool(s):
    l = s.lower()

    if l in TRUE_VALUES:
        return True
    elif l in FALSE_VALUES:
        return False

    return None


def get_bool(prop, t, default):
    if prop is None:
        return default

    out = prop

    if callable(prop):
        out = prop(t)
    elif isinstance(prop, (list, tuple)):
        out = pick_from_array(prop, t, False)
    elif isinstance(prop, str):
        return str2bool(prop)

    return out


def get_array(prop, t, default):
    if prop is None:
        return default

    if callable(prop):
        return prop(t)
    elif prop and (len(prop) == 2) and is_arr(prop[0]) and len(prop[0]) and is_arr(prop[1]) and len(prop[1]):
        # array of arrays
        arr0 = prop[0]
        arr1 = prop[1]
        length = min(len(arr0), len(arr1))
        result = []
        for i in range(length):
            v0 = arr0[i]
            v1 = arr1[i]
            result.append(lerp(t, v0, v1))
        return result
    elif prop and len(prop) > 1:
        return prop
    return default


def get_image(prop, t, default):
    if prop is None:
        return default
    elif callable(prop):
        return prop(t)
    elif is_arr(prop):
        return prop[clamp(floor(t * len(prop)), 0, len(prop) - 1)]
    return prop


def get_color(prop, t, default):
    if prop is None:
        return Color(default)

    out = None

    if callable(prop):
        out = prop(t)
    elif isinstance(prop, Color):
        out = prop
    elif is_arr(prop):
        if len(prop) == 2:
            out = clerp(t, Color(prop[0]), Color(prop[1]))
        elif len(prop) > 2:
            colors = map(Color, prop)
            out = multi_clerp(t, *colors)
        else:
            out = Color(prop[0])
    elif isinstance(prop, bool):
        out = prop
    else:
        out = Color(out)

    return out


_CAIRO_CONSTANTS = {
    "line_cap": {
        "butt": cairo.LINE_CAP_BUTT,
        "round": cairo.LINE_CAP_ROUND,
        "square": cairo.LINE_CAP_SQUARE
    },
    "line_join": {
        "miter": cairo.LINE_JOIN_MITER,
        "bevel": cairo.LINE_JOIN_BEVEL,
        "round": cairo.LINE_JOIN_ROUND
    },
    "antialias": {
        "default": cairo.ANTIALIAS_DEFAULT,
        "gray": cairo.ANTIALIAS_GRAY,
        "none": cairo.ANTIALIAS_NONE,
        "subpixel": cairo.ANTIALIAS_SUBPIXEL
    },
    "filter": {
        "best": cairo.FILTER_BEST,
        "bilinear": cairo.FILTER_BILINEAR,
        "fast": cairo.FILTER_FAST,
        "gaussian": cairo.FILTER_GAUSSIAN,
        "good": cairo.FILTER_GOOD,
        "nearest": cairo.FILTER_NEAREST,
    },
    "operator": {
        "add": cairo.OPERATOR_ADD,
        "atop": cairo.OPERATOR_ATOP,
        "clear": cairo.OPERATOR_CLEAR,
        "color_burn": cairo.OPERATOR_COLOR_BURN,
        "color_dodge": cairo.OPERATOR_COLOR_DODGE,
        "darken": cairo.OPERATOR_DARKEN,
        "dest": cairo.OPERATOR_DEST,
        "dest_atop": cairo.OPERATOR_DEST_ATOP,
        "dest_in": cairo.OPERATOR_DEST_IN,
        "dest_out": cairo.OPERATOR_DEST_OUT,
        "dest_over": cairo.OPERATOR_DEST_OVER,
        "difference": cairo.OPERATOR_DIFFERENCE,
        "hard_light": cairo.OPERATOR_HARD_LIGHT,
        "hsl_color": cairo.OPERATOR_HSL_COLOR,
        "hsl_hue": cairo.OPERATOR_HSL_HUE,
        "hsl_luminosity": cairo.OPERATOR_HSL_LUMINOSITY,
        "hsl_saturation": cairo.OPERATOR_HSL_SATURATION,
        "lighten": cairo.OPERATOR_LIGHTEN,
        "multiply": cairo.OPERATOR_MULTIPLY,
        "out": cairo.OPERATOR_OUT,
        "over": cairo.OPERATOR_OVER,
        "overlay": cairo.OPERATOR_OVERLAY,
        "saturate": cairo.OPERATOR_SATURATE,
        "screen": cairo.OPERATOR_SCREEN,
        "soft_light": cairo.OPERATOR_SOFT_LIGHT,
        "source": cairo.OPERATOR_SOURCE,
        "xor": cairo.OPERATOR_XOR
    }
}


def get_cairo_constant(name, prop, t, default):
    if prop is None:
        return default

    out = None

    if callable(prop):
        out = prop(t)
    elif isinstance(prop, str):
        out = _CAIRO_CONSTANTS[name.lower()][prop.lower()]
    else:
        out = prop

    return out
