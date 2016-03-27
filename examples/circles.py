from random import random

from example_util import get_filename
from glc.animation import Gif
from glc.color import Color


with Gif(get_filename(__file__)) as a:
    a.set_ease("linear").set_loop(False)
    l = a.render_list
    for i in range(40, 0, -1):
        f = "white"
        s = 20
        if i % 2 == 0:
            f = "black"
        l.circle(x=a.w * 0.5, y=a.h * 0.5, radius=[0 + (s * i), -40 + (s * i)], fill=Color(f), scale_y=0.5)
