"""

    glc.easing
    ==========

    Easing functions.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from math import pi, sin, cos, sqrt


def linear(t):
    return t


def sine(t):
    t = t * pi
    return 0.5 - cos(t) * 0.5


def quadratic(t):
    tt = 2 * t * t
    return tt if t <= 0.5 else -tt + (4 * t) - 1


def cubic(t):
    tt = 2 * t - 2
    return t * t * t * 4 if t <= 0.5 else 0.5 * (tt * tt * tt) + 1


def quartic(t):
    tt = t - 1
    return 8 * (t * t * t * t) if t <= 0.5 else -8 * (tt * tt * tt * tt) + 1


def quintic(t):
    t *= 2
    if t < 1:
        return (t * t * t * t * t) / 2
    t -= 2
    return (t * t * t * t * t + 2) / 2


def bounce(t):
    a = 0.36363636363636365
    b = 0.7272727272727273
    c = 0.9

    tt = t * t

    if t < a:
        return 7.5625 * tt
    if t < b:
        return 9.075 * tt - 9.9 * t + 3.4
    if t < c:
        ca = 12.066481994459833
        cb = 19.63545706371191
        cc = 8.898060941828255
        return ca * tt - cb * t + cc
    return 10.8 * tt - 20.52 * t + 10.72


def circular(t):
    return 0.5 * (1 - sqrt(1 - 4 * t * t)) if t <= 0.5 else 0.5 * (sqrt((3 - 2 * t) * (2 * t - 1)) + 1)


def exponential(t):
    if t == 0 or t == 1:
        return t
    return 0.5 * pow(2, (20 * t) - 10) if t <= 0.5 else -0.5 * pow(2, 10 - (t * 20)) + 1


def back(t):
    f = 1 - (2 * t - 1)
    if t <= 0.5:
        f = 2 * t
    g = (f * f * f) - f * sin(f * pi)

    if t <= 0.5:
        return 0.5 * g
    return 0.5 * (1 - g) + 0.5


def elastic(t):
    if t <= 0.5:
        return 0.5 * sin(13 * (pi * 0.5) * 2 * t) * pow(2, 10 * (2 * t - 1))
    return 0.5 * sin(-13 * (pi * 0.5) * ((2 * t - 1) + 1)) * pow(2, -10 * (2 * t - 1)) + 1


EASING_FUNCTIONS = {
    "linear": linear,
    "sine": sine,
    "quadratic": quadratic,
    "cubic": cubic,
    "quartic": quartic,
    "quintic": quintic,
    "bounce": bounce,
    "circular": circular,
    "exponential": exponential,
    "back": back,
    "elastic": elastic
}
