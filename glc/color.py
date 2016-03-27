"""

    glc.color
    =========

    Color manipulation tools.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from string import hexdigits
from colorsys import rgb_to_hsv, hsv_to_rgb, rgb_to_hls, hls_to_rgb
from math import floor, sin
from .utils import clamp, randrange
from .color_names import COLOR_NAMES


def rgb2hsv(red, green, blue):
    """Converts a color from RGB to HSV.

    Parameters
    ----------
    red : float
        Goes from 0.0 to 1.0.
    green : float
        Goes from 0.0 to 1.0.
    blue : float
        Goes from 0.0 to 1.0.

    Returns
    -------
    (hue, saturation, value) : tuple with 3 floats
    """
    hue, saturation, value = rgb_to_hsv(red, green, blue)
    return hue * 360, saturation, value


def hsv2rgb(hue, saturation, value):
    """Converts a color from HSV to RGB.

    Parameters
    ----------
    hue : float
        Goes from 0.0 to 360.0.
    saturation : float
        Goes from 0.0 to 1.0.
    value : float
        Goes from 0.0 to 1.0.

    Returns
    -------
    (red, green, blue) : tuple with 3 floats
    """
    return hsv_to_rgb(hue / 360, saturation, value)


def rgb2hsl(red, green, blue):
    """Converts a color from RGB to HSL.

    Parameters
    ----------
    red : float
        Goes from 0.0 to 1.0.
    green : float
        Goes from 0.0 to 1.0.
    blue : float
        Goes from 0.0 to 1.0.

    Returns
    -------
    (hue, saturation, lightness) : tuple with 3 floats
    """
    hue, lightness, saturation = rgb_to_hls(red, green, blue)
    return hue * 360, saturation, lightness


def hsl2rgb(hue, saturation, lightness):
    """Converts a color from HSV to RGB.

    Parameters
    ----------
    hue : float
        Goes from 0.0 to 360.0.
    saturation : float
        Goes from 0.0 to 1.0.
    lightness : float
        Goes from 0.0 to 1.0.

    Returns
    -------
    (red, green, blue) : tuple with 3 floats
    """
    return hls_to_rgb(hue / 360, lightness, saturation)


class Color:

    """Represents a color value.

    Attributes
    ----------
    r : float
        Amount of red, from 0.0 to 1.0.
    g : float
        Amount of green, from 0.0 to 1.0.
    b : float
        Amount of blue, from 0.0 to 1.0.
    a : float
        Alpha, from 0.0 to 1.0.
    """

    def __init__(self, r=None, g=None, b=None, a=None):
        if isinstance(r, str):
            self.r, self.g, self.b, self.a = str2color(r)
        elif isinstance(r, Color):
            self.r, self.g, self.b, self.a = r
        elif isinstance(r, int) and not all([g, b, a]):
            self.r, self.g, self.b, self.a = int2color(r)
        elif isinstance(r, (tuple, list)) and not all([g, b, a]):
            l = len(r)
            if l == 3:
                self.r, self.g, self.b = r
                self.a = 1
            elif l == 4:
                self.r, self.g, self.b, self.a = r
        else:
            self.r = r
            self.g = g
            self.b = b
            self.a = a

    def set_rgba(self, r, g, b, a=1.0):
        """Sets the current rgba values to the passed in ones.

        Parameters
        ----------
        r : float
            Amount of red, from 0.0 to 1.0.
        g : float
            Amount of green, from 0.0 to 1.0.
        b : float
            Amount of blue, from 0.0 to 1.0.
        a : float
            Alpha, from 0.0 to 1.0. Defaults to 1.0.

        Returns
        -------
        self
            For method chaining.
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        return self

    def set_int(self, color):
        """Sets the current color value based on the passed in integer.

        Parameters
        ----------
        color : int
            Normally passed in as a hex literal (i.e. 0xffff0000).
            The format expected is AARRGGBB.

        Returns
        -------
        self
            For method chaining.
        """
        a, r, g, b = color >> 24, color >> 16 & 0xff, color >> 8 & 0xff, color & 0xff
        self.a, self.r, self.g, self.b = a / 255, r / 255, g / 255, b / 255
        return self

    # grossly inefficient

    def desaturate(self, amount=10):
        """Desaturates this color by the given amount (a delta).

        Returns
        -------
        self
            For method chaining.
        """
        h, s, v = self.in_hsv()
        s = clamp(s - amount / 100, 0, 1)
        r, g, b = hsv2rgb(h, s, v)
        self.r, self.g, self.b = r, g, b
        return self

    def saturate(self, amount=10):
        """Saturates this color by the given amount (a delta).

        Returns
        -------
        self
            For method chaining.
        """
        h, s, v = self.in_hsv()
        s = clamp(s + amount / 100, 0, 1)
        r, g, b = hsv2rgb(h, s, v)
        self.r, self.g, self.b = r, g, b
        return self

    def grayscale(self):
        """Desaturates this color until it is a shade of gray.

        Returns
        -------
        self
            For method chaining.
        """
        return self.desaturate(100)

    def lighten(self, amount=10):
        """Lightens up this color by the given amount (a delta).

        Returns
        -------
        self
            For method chaining.
        """
        h, s, l = self.in_hsl()
        l = clamp(l + amount / 100, 0, 1)
        r, g, b = hsl2rgb(h, s, l)
        self.r, self.g, self.b = r, g, b
        return self

    def darken(self, amount=10):
        """Darkens up this color by the given amount (a delta).

        Returns
        -------
        self
            For method chaining.
        """
        h, s, l = self.in_hsl()
        l = clamp(l - amount / 100, 0, 1)
        r, g, b = hsl2rgb(h, s, l)
        self.r, self.g, self.b = r, g, b
        return self

    def in_hsv(self):
        """Returns this color in HSV, as a tuple."""
        return rgb2hsv(self.r, self.g, self.b)

    def in_hsl(self):
        """Returns this color in HSL, as a tuple."""
        return rgb2hsl(self.r, self.g, self.b)

    def in_int(self):
        """Returns this color as a single integer, in the format AA RR GG BB."""
        r = floor(self.r * 255)
        g = floor(self.g * 255)
        b = floor(self.b * 255)
        a = floor(self.a * 255)
        return a << 24 | r << 16 | g << 8 | b

    def brightness(self):
        """Returns the overall brightness for this color.

        Adapted from http://www.w3.org/TR/AERT#color-contrast
        """
        r, g, b = map(floor, [self.r * 255, self.g * 255, self.b * 255])
        return ((r * 299) + (g * 587) + (b * 114)) / 1000

    def luminance(self):
        """Returns the overall luminance for this color.

        Adapted from http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
        """
        r = self.r / 12.92 if self.r <= 0.03928 else pow(((self.r + 0.055) / 1.055), 2.4)
        g = self.g / 12.92 if self.g <= 0.03928 else pow(((self.g + 0.055) / 1.055), 2.4)
        b = self.b / 12.92 if self.b <= 0.03928 else pow(((self.b + 0.055) / 1.055), 2.4)
        return (0.2126 * r) + (0.7152 * g) + (0.0722 * b)

    def __getitem__(self, index):
        return (self.r, self.g, self.b, self.a)[index]

    def __int__(self):
        return self.in_int()

    def __repr__(self):
        return "rgba({0.r}, {0.g}, {0.b}, {0.a})".format(self)


# shortcuts

def rgba(red, green, blue, alpha=1.0):
    """Creates a color using the passed in red, green, blue and alpha values.

    Parameters
    ----------
    red : float
    green : float
    blue : float
    alpha : float

    Returns
    -------
    :class:`Color`
    """
    return Color(red, green, blue, alpha)


def hsva(h, s, v, a=1.0):
    """Creates a color using hue, saturation, value and alpha.

    Parameters
    ----------
    h : float
    s : float
    v : float
    a : float

    Returns
    -------
    :class:`Color`
    """
    r, g, b = hsv2rgb(h, s, v)
    return Color(r, g, b, a)


def gray(shade, alpha=1.0):
    """Creates a shade of gray.

    Parameters
    ----------
    shade : float
    alpha : float

    Returns
    -------
    :class:`Color`
    """
    return Color(shade, shade, shade, alpha)


def random_rgba(min_red, max_red, min_green, max_green, min_blue, max_blue, min_alpha=None, max_alpha=None):
    """Creates a random color using the passed in ranges for red, green, blue and alpha.

    If ``min_alp`` and ``max_alp`` are left as ``None``, then alpha is simply set to 1.

    Parameters
    ----------
    min_red : float
    max_red : float
    min_green : float
    max_green : float
    min_blue : float
    max_blue : float
    min_alpha : float
    max_alpha : float

    Returns
    -------
    :class:`Color`
    """

    alpha = 1
    if min_alpha is not None and max_alpha is not None:
        alpha = randrange(min_alpha, max_alpha)

    return Color(
        randrange(min_red, max_red),
        randrange(min_green, max_green),
        randrange(min_blue, max_blue),
        alpha
    )


def random_gray(min_shade, max_shade, min_alpha=None, max_alpha=None):
    """Creates a random shade of grey.

    If ``min_alp`` and ``max_alp`` are left as ``None``, then alpha is simply set to 1.

    Parameters
    ----------
    min_shade : float
    max_shade : float
    min_alpha : float
    max_alpha : float
        The ranges to generate random values from.

    Returns
    -------
    :class:`Color`
    """

    alpha = 1
    if min_alpha is not None and max_alpha is not None:
        alpha = randrange(min_alpha, max_alpha)

    return gray(randrange(min_shade, max_shade), alpha)


def random_hsva(min_hue, max_hue, min_saturation, max_saturation, min_value, max_value, min_alpha=None, max_alpha=None):
    """Creates a random color using the passed in ranges for hue, saturation, value and alpha.

    If ``min_alp`` and ``max_alp`` are left as ``None``, then alpha is simply set to 1.

    Parameters
    ----------
    min_hue : float
    max_hue : float
    min_saturation : float
    max_saturation : float
    min_value : float
    max_value : float
    min_alpha : float
    max_alpha : float

    Returns
    -------
    :class:`Color`
    """

    alpha = 1
    if min_alpha is not None and max_alpha is not None:
        alpha = randrange(min_alpha, max_alpha)

    return hsva(
        randrange(min_hue, max_hue),
        randrange(min_saturation, max_saturation),
        randrange(min_value, max_value),
        alpha
    )


def name2color(name):
    """Creates a color based on a name.

    If no color is found, black is returned.

    The recognized names can be found here: https://en.wikipedia.org/wiki/X11_color_names

    Returns
    -------
    :class:`Color`
    """
    return rgba(*COLOR_NAMES.get(name.lower(), (0.0, 0.0, 0.0)))


def int2color(color):
    """Creates a color based on an integer.

    Parameters
    ----------
    color : int
        The format is AARRGGBB.

    Returns
    -------
    :class:`Color`
    """
    return Color().set_int(color)


def str2color(string):
    """Creates a color based on a string.

    Parameters
    ----------
    color : string
        Can be one of the following:

        - Color value in base 16/hex.
            The format is ``[#/0x][AA]R[R]G[G]B[B]``.

        - CSS/X11 color name (see https://en.wikipedia.org/wiki/X11_color_names)

    Returns
    -------
    :class:`Color`
    """

    # strip hex notation, if it's there
    if string.startswith("0x"):
        string = string[2:]
    elif string.startswith("#"):
        string = string[1:]

    if all(char in hexdigits for char in string):
        length = len(string)

        if length == 8:  # aarrggbb
            return (
                int(string[2:4], 16) / 255,
                int(string[4:6], 16) / 255,
                int(string[6:8], 16) / 255,
                int(string[0:2], 16) / 255
            )
        elif length == 6:  # rrggbb
            return rgba(
                int(string[0:2], 16) / 255,
                int(string[3:4], 16) / 255,
                int(string[5:6], 16) / 255
            )
        elif length == 4:  # argb
            return rgba(
                int(string[1] * 2, 16) / 255,
                int(string[2] * 2, 16) / 255,
                int(string[3] * 2, 16) / 255,
                int(string[0] * 2, 16) / 255
            )
        else:  # rgb
            return rgba(
                int(string[0] * 2, 16) / 255,
                int(string[1] * 2, 16) / 255,
                int(string[2] * 2, 16) / 255,
            )
    else:  # X11/css name
        return name2color(string)


# utils

def clerp(t, color_a, color_b):
    """Linearly interpolates from color_a to color_b by t.

    Parameters
    ----------
    t : float
        A number from 0.0 to 1.0.
    color_a : Color
    color_b : Color
        The colors to interpolate.

    Returns
    -------
    Color
    """
    return rgba(
        color_a.r + (color_b.r - color_a.r) * t,
        color_a.g + (color_b.g - color_a.g) * t,
        color_a.b + (color_b.b - color_a.b) * t,
        color_a.a + (color_b.a - color_a.a) * t
    )


def multi_clerp(t, *colors):
    """Linearly interpolates between an array of colors by t.

    Parameters
    ----------
    t : float
        A number from 0.0 to 1.0.
    colors : iterable with Color objects
        The colors to interpolate.

    Returns
    -------
    Color
    """
    l = len(colors) - 1
    tt = t * (l)
    prev_index, next_index = clamp(floor(tt), 0, l), clamp(floor(tt) + 1, 0, l)
    prev_color, next_color = colors[prev_index], colors[next_index]
    ttt = tt - floor(tt)

    return clerp(ttt, prev_color, next_color)


def sinebow(offset, freq0, freq1, freq2, phase0, phase1, phase2, center=128, width=127):
    """Returns a color based on a 'sinebow'.

    See http://krazydad.com/tutorials/makecolors.php
    """
    red = sin(freq0 * offset + phase0) * width + center
    green = sin(freq1 * offset + phase1) * width + center
    blue = sin(freq2 * offset + phase2) * width + center
    return rgba(red / 255, green / 255, blue / 255)


def hue_split(base_color, split_num=6):
    """Returns variations of a color by moving its hue around the "color wheel"."""
    dr = 360 / split_num
    h, s, v = base_color.in_hsv()
    return tuple(hsva(h + i * dr, s, v) for i in range(split_num))


def complementaries(base_color):
    """Returns colors that are opposite each other on the color wheel."""
    return hue_split(base_color, 2)


def split_complementaries(base_color, angle=30):
    """Returns the base color and two colors adjacent to its complement."""
    h, s, v = base_color.in_hsv()
    return (hsva(h, s, v), hsva(h + 180 - angle, s, v), hsva(h + 180 + angle, s, v))


def triads(base_color):
    """Returns 3 colors that are evenly spaced around the color wheel."""
    return hue_split(base_color, 3)


def tetrads(base_color):
    """Returns four colors arranged into two complementary pairs."""
    return hue_split(base_color, 4)


def pentads(base_color):
    """Returns 5 colors arranged into a pentagon on the color wheel."""
    return hue_split(base_color, 5)


def hexads(base_color):
    """Returns 6 colors arranged into a hexagon on the color wheel."""
    return hue_split(base_color, 6)
