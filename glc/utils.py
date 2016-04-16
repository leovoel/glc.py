"""

    glc.utils
    =========

    Miscellaneous helpers.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from bisect import bisect_left
from math import sqrt, sin, cos, tan, acos, pi, floor, degrees, radians
from random import random
from PIL import Image

import re

# math utils

deg = degrees
rad = radians


def clamp(value, start, end):
    """Limits a value to the passed in range.

    If ``value`` is less than ``start``, ``start`` is returned.
    If ``value`` is greater than ``end``, ``end`` is returned.
    Otherwise, ``value`` is returned.

    Returns
    -------
    float
        The clamped value.
    """
    return start if value < start else end if value > end else value


def norm(value, start, end):
    """Normalizes a value in the range specified by ``start`` and ``end`` to the range 0-1.

    Returns
    -------
    float
        The normalized value.
    """
    return (value - start) / (end - start)


def lerp(t, start, end):
    """Linearly interpolates from ``start`` to ``end`` by ``t``.

    Returns
    -------
    float
        The interpolated value.
    """
    return (end - start) * t + start


def remap(value, src_min, src_max, dst_min, dst_max):
    """Maps a value from a source range to a target range.

    Returns
    -------
    float
        The remapped value.
    """
    return lerp(norm(value, src_min, src_max), dst_min, dst_max)


def randrange(start, end):
    """Returns a random float in the range defined by ``start`` and ``end``.

    Returns
    -------
    float
        The random value.
    """
    return start + random() * (end - start)


def bezier(v, x0, x1, x2, x3):
    """Returns a point for a given ``v`` value on the specified cubic bézier path.

    Returns
    -------
    float
        The point on the 1D path.
    """
    return (1 - v) * (1 - v) * (1 - v) * x0 + 3 * (1 - v) * (1 - v) * v * x1 + 3 * (1 - v) * v * v * x2 + v * v * v * x3


def quadratic(v, x0, x1, x2):
    """Returns a point for a given ``v`` value on the specified quadratic bézier path.

    Returns
    -------
    float
        The point on the 1D path.
    """
    return (1 - v) * (1 - v) * x0 + 2 * (1 - v) * v * x1 + v * v * x2


def catmull_rom(v, x0, x1, x2, x3):
    """Returns a point for a given ``v`` value on the specified Catmull-Rom spline.

    Returns
    -------
    float
        The point on the 1D path.
    """
    return (0.5 * (2 * x1 + (x2 - x0) * v + (2 * x0 - 5 * x1 + 4 * x2 - x3) * v * v + (3 * x1 - x0 - 3 * x2 + x3) * v * v * v))


def spline(v, x0, x1, x2, x3, tightness=1):
    v0 = tightness * (x2 - x0) * 0.5
    v1 = tightness * (x3 - x1) * 0.5
    return v * v * v * (2 * x1 - 2 * x2 + v0 + v1) + v * v * (-3 * x1 + 3 * x2 - 2 * v0 - v1) + v0 * v + x1


def quantize(value, tick):
    """Rounds the given ``value`` to the nearest multiple of ``tick``.

    Returns
    -------
    float
        The quantized value.
    """
    return tick * floor(value / tick)


def distribute(divisions, start=0, end=1, inclusive=False):
    """Returns a range of values between ``start`` and ``end``, divided in the wanted amount of pieces.

    Parameters
    ----------
    divisions : int
        How many pieces should the range be broken in.
    start : float
        The value to start at.
    end : float
        The value to end at.
    inclusive : bool
        Whether the end should be included in the distribution.

    Returns
    -------
    Generator of floats
        The distribution of values.
    """
    d = end - start
    return (d * (i / divisions) + start for i in range(0, divisions + int(inclusive)))


def hermite(v, x0, x1, x2, x3):
    """Returns a value ``v`` interpolated using hermite interpolation.

    Returns
    -------
    float
        The interpolated value.
    """
    if v == 0:
        return x0
    elif v == 1:
        return x2
    else:
        return (2 * x0 - 2 * x2 + x3 + x1) * v * v * v + (3 * x2 - 3 * x0 - 2 * x1 - x3) * v * v + x1 * v + x0


def cosine(value, start, end):
    """Interpolates a ``value`` from ``start`` to ``end`` using cosine interpolation.

    Returns
    -------
    float
        The interpolated value.
    """
    value2 = (1 - cos(value * pi)) / 2
    return start * (1 - value2) + end * value2


def smoothstep(value, start, end):
    """Interpolate a ``value`` from ``start`` to ``end`` using the smoothstep function.

    See https://en.wikipedia.org/wiki/Smoothstep

    Returns
    -------
    float
        The interpolated value.
    """
    x = clamp(norm(value, start, end), 0, 1)
    return x * x * (3 - 2 * x)


def smootherstep(value, start, end):
    """Interpolate a ``value`` from ``start`` to ``end`` using the smootherstep function.

    See https://en.wikipedia.org/wiki/Smoothstep#Variations

    Returns
    -------
    float
        The interpolated value.
    """
    x = clamp(norm(value, start, end), 0, 1)
    return x * x * x * (x * (x * 6 - 15) + 10)


def pick_closest(n, l):
    """Pick a value from an iterable ``l`` at index ``n``, which is "snapped back" to a valid index.

    Parameters
    ----------
    n : int
        Index to round.
    l : iterable
        Iterable to pick a value from.

    Returns
    -------
    Iterable element
        Whatever was at the picked index in the iterable.
    """
    position = bisect_left(l, n)
    if position == 0:
        return l[0]
    if position == len(l):
        return l[-1]
    before = l[position - 1]
    after = l[position]
    if after - n < n - before:
        return after
    return before


# cairo utils

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
        The image in bytes.
    """
    size = surface.get_width(), surface.get_height()
    img = Image.frombuffer('RGBA', size, bytes(surface.get_data()), 'raw', 'BGRA', 0, 1)
    return img.tobytes('raw', 'RGBA', 0, 1)


def draw_image(ctx, img, x, y, w=None, h=None):
    """Draws an image on a given Cairo context.

    If given explicit width and height, the image is resized
    to fit those dimensions, without any regard for maintaining
    aspect ratio or anything like that.

    If you want that kind of behavior, you'll have
    to calculate the desired width and height a priori.

    Parameters
    ----------
    ctx : :class:`cairo.Context`
        The context to draw an image on.
    img : :class:`cairo.Surface`
        The image (as a Cairo surface) to draw.
    x : float
        Horizontal position to draw the image on.
    y : float
        Vertical position to draw the image on.
    w : float
        Target width for the image.
    h : float
        Target height for the image.
    """
    sourcew, sourceh = img.get_width(), img.get_height()

    if w is None:
        w = sourcew
    if h is None:
        h = sourceh

    ctx.save()

    ctx.translate(x, y)
    ctx.scale(w / sourcew, h / sourceh)

    ctx.set_source_surface(img, 0, 0)
    ctx.paint()

    ctx.restore()


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


def curve_path(context, points, loop=False):
    """Defines a path with multiple points connected by quadratic bézier curves.

    Parameters
    ----------
    context : :class:`cairo.Context`
        The context to draw a curve on.
    points : list of tuples/lists
        Specifies the coordinates to plot the curve with.
    loop : bool
        Specifies whether the path should be closed by connecting the first
        point with the last one or not. Defaults to ``False``.
    """
    l = len(points)
    mid_points = []
    i = 0
    while i < l - 1:
        mid_points.append((
            (points[i][0] + points[i + 1][0]) * 0.5,
            (points[i][1] + points[i + 1][1]) * 0.5
        ))
        i += 1

    if loop:
        mid_points.append((
            (points[i][0] + points[0][0]) * 0.5,
            (points[i][1] + points[0][1]) * 0.5
        ))

        context.move_to(mid_points[0][0], mid_points[0][1])

        i = 1
        while i < l:
            quadratic_curve_to(context, points[i][0], points[i][1], mid_points[i][0], mid_points[i][1])
            i += 1

        quadratic_curve_to(context, points[0][0], points[0][1], mid_points[0][0], mid_points[0][1])
    else:
        context.move_to(points[0][0], points[0][1])

        i = 1
        while i < l - 2:
            quadratic_curve_to(context, points[i][0], points[i][1], mid_points[i][0], mid_points[i][1])
            i += 1

        quadratic_curve_to(context, points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])


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

# string utils

# TODO: expand into more robust emoji check

_EMOJI_RANGE_RE = re.compile('[\U00010000-\U0010ffff]')


def is_emoji(s):
    return _EMOJI_RANGE_RE.match(s)
