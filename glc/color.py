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

    All the color components here should go from 0.0 to 1.0.

    Parameters
    ----------
    red : float
    green : float
    blue : float

    Returns
    -------
    (hue, saturation, value) : tuple with 3 floats
    """
    hue, saturation, value = rgb_to_hsv(red, green, blue)
    return hue * 360, saturation, value


def hsv2rgb(hue, saturation, value):
    """Converts a color from HSV to RGB.

    All the color components here should go from 0.0 to 1.0,
    except for hue, which should go from 0.0 to 360.

    Parameters
    ----------
    hue : float
    saturation : float
    value : float

    Returns
    -------
    (red, green, blue) : tuple with 3 floats
    """
    return hsv_to_rgb(hue / 360, saturation, value)


def rgb2hsl(red, green, blue):
    """Converts a color from RGB to HSL.

    All the color components here should go from 0.0 to 1.0.

    Parameters
    ----------
    red : float
    green : float
    blue : float

    Returns
    -------
    (hue, saturation, lightness) : tuple with 3 floats
    """
    hue, lightness, saturation = rgb_to_hls(red, green, blue)
    return hue * 360, saturation, lightness


def hsl2rgb(hue, saturation, lightness):
    """Converts a color from HSV to RGB.

    All the color components here should go from 0.0 to 1.0,
    except for hue, which should go from 0.0 to 360.

    Parameters
    ----------
    hue : float
    saturation : float
    lightness : float

    Returns
    -------
    (red, green, blue) : tuple with 3 floats
    """
    return hls_to_rgb(hue / 360, lightness, saturation)


class Color:

    """Represents a color value.

    All the color components here go from 0.0 to 1.0.

    Attributes
    ----------
    r : float
    g : float
    b : float
    a : float
    """

    def __init__(self, r=None, g=None, b=None, a=None):
        if isinstance(r, str):
            self.r, self.g, self.b, self.a = str2color(r)
        elif isinstance(r, Color):
            self.r, self.g, self.b, self.a = r
        elif isinstance(r, int) and all((c is None for c in [g, b, a])):
            self.r, self.g, self.b, self.a = int2color(r)
        elif isinstance(r, (tuple, list)):
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

        All the color components here should go from 0.0 to 1.0.
        If no value for alpha (``a``) is passed in, then 1.0 is
        used as the default.

        Parameters
        ----------
        r : float
        g : float
        b : float
        a : float

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

        Parameters
        ----------
        amount : float
            Amount to desaturate this color by.
            Should go from 0.0 to 100.0.

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

        Parameters
        ----------
        amount : float
            Amount to saturate this color by.
            Should go from 0.0 to 100.0.

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

        Parameters
        ----------
        amount : float
            Amount to lighten this color by.
            Should go from 0.0 to 100.0.

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

        Parameters
        ----------
        amount : float
            Amount to darken this color by.
            Should go from 0.0 to 100.0.

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

    All the color components here should go from 0.0 to 1.0.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    return Color(red, green, blue, alpha)


def hsva(hue, saturation, value, alpha=1.0):
    """Creates a color using hue, saturation, value and alpha.

    All the color components here should go from 0.0 to 1.0,
    except for hue, which should go from 0.0 to 360.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    red, green, blue = hsv2rgb(hue, saturation, value)
    return Color(red, green, blue, alpha)


def gray(shade, alpha=1.0):
    """Creates a shade of gray.

    All the color components here should go from 0.0 to 1.0.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    return Color(shade, shade, shade, alpha)


def random_rgba(min_red, max_red, min_green, max_green, min_blue, max_blue, min_alpha=None, max_alpha=None):
    """Creates a random color using the passed in ranges for red, green, blue and alpha.

    All the color components here should go from 0.0 to 1.0.

    If ``min_alp`` and ``max_alp`` are left as ``None``, then alpha is simply set to 1.0.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """

    alpha = 1.0
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

    All the color components here should go from 0.0 to 1.0.

    If ``min_alp`` and ``max_alp`` are left as ``None``, then alpha is simply set to 1.0.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """

    alpha = 1.0
    if min_alpha is not None and max_alpha is not None:
        alpha = randrange(min_alpha, max_alpha)

    return gray(randrange(min_shade, max_shade), alpha)


def random_hsva(min_hue, max_hue, min_saturation, max_saturation, min_value, max_value, min_alpha=None, max_alpha=None):
    """Creates a random color using the passed in ranges for hue, saturation, value and alpha.

    All the color components here should go from 0.0 to 1.0,
    except for hue, which should go from 0.0 to 360.

    If ``min_alp`` and ``max_alp`` are left as ``None``, then alpha is simply set to 1.0.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """

    alpha = 1.0
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

    If the passed in name is not recognized, black is returned.

    The recognized names can be found here: https://en.wikipedia.org/wiki/X11_color_names

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    return rgba(*COLOR_NAMES.get(name.lower(), (0.0, 0.0, 0.0)))


def int2color(color):
    """Creates a color based on an integer.

    Parameters
    ----------
    color : int
        Usually you'll want to pass a hex literal (e.g. ``0xFFFF00AE``).
        The expected format is AARRGGBB.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    return Color().set_int(color)


def str2color(string):
    """Creates a color based on a string.

    Parameters
    ----------
    color : string
        Can be one of the following:

        - Color value in base 16/hex.
            The format is ``[#/0x][[A]A]R[R]G[G]B[B]``.
            If you pass just one digit for each color value, the value is used twice.
            (e.g. for R G B, the digits are duplicated so it becomes RR GG BB)
            Alpha is optional, and so are the 0x/# hex identifiers.

        - CSS/X11 color name (see https://en.wikipedia.org/wiki/X11_color_names)

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """

    # strip hex notation, if it's there
    if string.startswith("0x"):
        string = string[2:]
    elif string.startswith("#"):
        string = string[1:]

    if all(char in hexdigits for char in string):
        length = len(string)

        if length == 8:  # aarrggbb
            return rgba(
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
    color_a : :class:`Color`
        The color to interpolate from.
    color_b : :class:`Color`
        The color to interpolate to.

    Returns
    -------
    color : :class:`Color`
        A Color object.
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
    colors : iterable with :class:`Color` objects
        The colors to interpolate.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    l = len(colors) - 1
    tt = t * (l)
    prev_index, next_index = clamp(floor(tt), 0, l), clamp(floor(tt) + 1, 0, l)
    prev_color, next_color = colors[prev_index], colors[next_index]
    ttt = tt - floor(tt)

    return clerp(ttt, prev_color, next_color)


def sinebow(offset, freq0, freq1, freq2, phase0, phase1, phase2, center=128, width=127):
    """Returns a color based on a 'sinebow'.

    See http://krazydad.com/tutorials/makecolors.php for more info.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    red = sin(freq0 * offset + phase0) * width + center
    green = sin(freq1 * offset + phase1) * width + center
    blue = sin(freq2 * offset + phase2) * width + center
    return rgba(red / 255, green / 255, blue / 255)


def hue_split(base_color, split_num=6):
    """Returns variations of a color by moving its hue around the "color wheel".

    Parameters
    ----------
    base_color : :class:`Color`
        The color to split by hue.
    split_num : int
        How many times this color should be split around the color wheel.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    dr = 360 / split_num
    h, s, v = base_color.in_hsv()
    return tuple(hsva(h + i * dr, s, v) for i in range(split_num))


def complementaries(base_color):
    """Returns colors that are opposite each other on the color wheel.

    Parameters
    ----------
    base_color : :class:`Color`
        The color to find the complementary of.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    return hue_split(base_color, 2)


def split_complementaries(base_color, angle=30):
    """Returns the base color and two colors adjacent to its complement.

    Parameters
    ----------
    base_color : :class:`Color`
        The color to find the complementaries of.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    h, s, v = base_color.in_hsv()
    return (hsva(h, s, v), hsva(h + 180 - angle, s, v), hsva(h + 180 + angle, s, v))


def triads(base_color):
    """Returns 3 colors that are evenly spaced around the color wheel.

    Parameters
    ----------
    base_color : :class:`Color`
        The color to base the traids from.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    return hue_split(base_color, 3)


def tetrads(base_color):
    """Returns four colors arranged into two complementary pairs.

    Parameters
    ----------
    base_color : :class:`Color`
        The color to base the tetrads from.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    return hue_split(base_color, 4)


def pentads(base_color):
    """Returns 5 colors arranged into a pentagon on the color wheel.

    Parameters
    ----------
    base_color : :class:`Color`
        The color to base the pentads from.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    return hue_split(base_color, 5)


def hexads(base_color):
    """Returns 6 colors arranged into a hexagon on the color wheel.

    Parameters
    ----------
    base_color : :class:`Color`
        The color to base the hexads from.

    Returns
    -------
    color : :class:`Color`
        A Color object.
    """
    return hue_split(base_color, 6)
