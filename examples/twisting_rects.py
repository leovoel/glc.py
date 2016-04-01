from random import random

from example_util import get_filename
from glc import Gif
from glc.color import rgba, hsva


with Gif(get_filename(__file__), color_count=8) as a:
    a.set_size(400, 400).set_duration(2).set_fps(30)
    l = a.render_list
    l.rect(
        x=a.w / 2,
        y=a.h / 2,
        w=a.w,
        h=a.h,
        fill=rgba(20 / 255, 50 / 255, 10 / 255)
    )

    res = 40
    y = 0
    while y < a.h:
        x = 0
        while x < a.w:
            l.rect(
                translation_x=x,
                translation_y=y,
                x=res / 2,
                y=res / 2,
                w=[res * 2, 0],
                h=[0, res * 2],
                phase=1.99 * (y + x) * 0.2,
                fill=hsva(((x + y) / 5) * 90 + 50, 0.8, 1),
                stroke=False
            )
            x += res * 0.7
        y += res * 0.5
