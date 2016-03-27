"""

    glc.utils
    =========

    Miscellaneous helpers.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import sqrt, sin, cos, tan, acos, pi, floor
from random import random
from PIL import Image


DEGTORAD = pi / 180
RADTODEG = 180 / pi


def deg(rad):
    return rad * RADTODEG


def rad(deg):
    return deg * DEGTORAD


def clamp(value, start, end):
    return start if value < start else end if value > end else value


def norm(value, start, end):
    return (value - start) / (end - start)


def lerp(t, start, end):
    return (end - start) * t + start


def remap(value, src_min, src_max, dst_min, dst_max):
    return lerp(norm(value, src_min, src_max), dst_min, dst_max)


def randrange(start, end):
    return start + random() * (end - start)


def bezier(v, x0, x1, x2, x3):
    return (1 - v) * (1 - v) * (1 - v) * x0 + 3 * (1 - v) * (1 - v) * v * x1 + 3 * (1 - v) * v * v * x2 + v * v * v * x3


def quadratic(v, x0, x1, x2):
    return (1 - v) * (1 - v) * x0 + 2 * (1 - v) * v * x1 + v * v * x2


def catmull_rom(v, x0, x1, x2, x3):
    return (0.5 * (2 * x1 + (x2 - x0) * v + (2 * x0 - 5 * x1 + 4 * x2 - x3) * v * v + (3 * x1 - x0 - 3 * x2 + x3) * v * v * v))


def spline(v, x0, x1, x2, x3, tightness=1):
    v0 = tightness * (x2 - x0) * 0.5
    v1 = tightness * (x3 - x1) * 0.5
    return v * v * v * (2 * x1 - 2 * x2 + v0 + v1) + v * v * (-3 * x1 + 3 * x2 - 2 * v0 - v1) + v0 * v + x1


def quantize(value, tick):
    return tick * floor(value / tick)


def distribute(divisions, start=0, end=1, inclusive=False):
    d = end - start
    return (d * (i / divisions) + start for i in range(0, divisions + int(inclusive)))


def hermite(v, x0, x1, x2, x3):
    if v == 0:
        return x0
    elif v == 1:
        return x2
    else:
        return (2 * x0 - 2 * x2 + x3 + x1) * v * v * v + (3 * x2 - 3 * x0 - 2 * x1 - x3) * v * v + x1 * v + x0


def cosine(value, start, end):
    value2 = (1 - cos(value * pi)) / 2
    return start * (1 - value2) + end * value2


def smoothstep(value, start, end):
    x = clamp(norm(value, start, end), 0, 1)
    return x * x * (3 - 2 * x)


def smootherstep(value, start, end):
    x = clamp(norm(value, start, end), 0, 1)
    return x * x * x * (x * (x * 6 - 15) + 10)


def bgra_to_rgba(surface):
    """Converts a Cairo surface color format from BGRA to RGBA, using Pillow/PIL.

    On little-endian machines, Cairo's surface format becomes BGRA instead of RGBA.
    When creating numpy arrays with the data from the surface, the colors end up
    wrong if we don't do this conversion.

    Adapted from http://www.pygame.org/wiki/CairoPygame (thanks!)

    Parameters
    ----------
    surface : :class:`cairo.Surface`
        The cairo surface to convert.

    Returns
    -------
    img_bytes : bytes object
    """

    size = surface.get_width(), surface.get_height()
    img = Image.frombuffer('RGBA', size, bytes(surface.get_data()), 'raw', 'BGRA', 0, 1)
    return img.tobytes('raw', 'RGBA', 0, 1)


def quadratic_curve_to(context, x1, y1, x2, y2):
    """Adds a quadratic Bézier spline to the path from
    the current point to position (x2, y2) in user-space
    coordinates, using (x1, y1) as the control point.

    After this call the current point will be (x2, y2).

    If there is no current point before the call to curve_to()
    this method will behave as if preceded by a call
    to context.move_to(x1, y1).

    Parameters
    ----------
    context : :class:`cairo.Context`
        The context to draw on.
    x2 : float
        The X coordinate of the first control point.
    y2 : float
        The Y coordinate of the first control point.
    x3 : float
        The X coordinate of the end of the curve.
    y3 : float
        The Y coordinate of the end of the curve.
    """
    x0, y0 = context.get_current_point()

    if x0 == 0 and y0 == 0:
        x0 = x1
        y0 = y1

    context.curve_to(
        x0 + 2 / 3 * (x1 - x0),
        y0 + 2 / 3 * (y1 - y0),
        x2 + 2 / 3 * (x1 - x2),
        y2 + 2 / 3 * (y1 - y2),
        x2, y2
    )


def arc_to(context, x1, y1, x2, y2, r):
    """Adds an arc to the path with the given control points and radius,
    connected to the previous point by a straight line.

    After this call the current point will be (x2, y2).

    Parameters
    ----------
    context : :class:`cairo.Context`
        The context to draw on.
    x1 : float
        The x axis of the coordinate for the first control point.
    y1 : float
        The y axis of the coordinate for the first control point.
    x2 : float
        The x axis of the coordinate for the second control point.
    y2 : float
        The y axis of the coordinate for the second control point.
    radius : float
        The arc's radius.
    """

    x0, y0 = context.get_current_point()
    if (
        x1 == x0 and y1 == y0 or
        x1 == x2 and y1 == y2 or
        r == 0
    ):
        context.line_to(x1, y1)
        return

    x1x0, y1y0 = x0 - x1, y0 - y1
    x1x2, y1y2 = x2 - x1, y2 - y1
    p1p0_length = sqrt(x1x0 * x1x0 + y1y0 * y1y0)
    p1p2_length = sqrt(x1x2 * x1x2 + y1y2 * y1y2)

    cos_phi = (x1x0 * x1x2 + y1y0 * y1y2) / (p1p0_length * p1p2_length)

    if cos_phi == -1:
        context.line_to(x1, y1)
        return

    if cos_phi == 1:
        max_length = 65535
        factor_max = max_length / p1p0_length
        context.line_to(x0 + factor_max * x1x0, y0 + factor_max * y1y0)
        return

    tangent = r / tan(acos(cos_phi) / 2)
    factor_p1p0 = tangent / p1p0_length
    t_x1x0, t_y1y0 = x1 + factor_p1p0 * x1x0, y1 + factor_p1p0 * y1y0

    orth_x1x0, orth_y1y0 = y1y0, -x1x0
    orth_p1p0_length = sqrt(orth_x1x0 * orth_x1x0 + orth_y1y0 * orth_y1y0)
    factor_ra = r / orth_p1p0_length

    cos_alpha = (orth_x1x0 * x1x2 + orth_y1y0 * y1y2) / (orth_p1p0_length * p1p2_length)
    if cos_alpha < 0:
        orth_x1x0, orth_y1y0 = -orth_x1x0, -orth_y1y0

    px, py = t_x1x0 + factor_ra * orth_x1x0, t_y1y0 + factor_ra * orth_y1y0
    orth_x1x0, orth_y1y0 = -orth_x1x0, -orth_y1y0
    sa = acos(orth_x1x0 / orth_p1p0_length)
    if orth_y1y0 < 0:
        sa = 2 * pi - sa

    anticlockwise = False

    factor_p1p2 = tangent / p1p2_length
    t_x1x2, t_y1y2 = x1 + factor_p1p2 * x1x2, y1 + factor_p1p2 * y1y2
    orth_x1x2, orth_y1y2 = t_x1x2 - px, t_y1y2 - py
    orth_p1p2_length = sqrt(orth_x1x2 * orth_x1x2 + orth_y1y2 * orth_y1y2)
    ea = acos(orth_x1x2 / orth_p1p2_length)

    if orth_y1y2 < 0:
        ea = 2 * pi - ea

    if (sa > ea) and ((sa - ea) < pi):
        anticlockwise = True

    if (sa < ea) and ((ea - sa) > pi):
        anticlockwise = True

    context.line_to(t_x1x0, t_y1y0)

    if anticlockwise and pi * 2 != r:
        context.arc_negative(px, py, r, sa, ea)
        return

    context.arc(px, py, r, sa, ea)
