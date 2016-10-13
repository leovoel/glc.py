from example_util import get_filename
from glc.utils import remap
from glc import Gif


with Gif(get_filename(__file__)) as a:
    l = a.render_list
    w, h = a.w, a.h
    r = 20

    iv = "linear quadratic cubic quartic quintic sine bounce circular exponential back elastic".split()
    length = len(iv)

    for i in range(length):
        l.circle(
            x=remap(i + 1, 1, length, r, w - r),
            y=[500 * 0.5 - 100, 500 * 0.5 + 100],
            radius=r
        ).ease = iv[i]

    a.save()
