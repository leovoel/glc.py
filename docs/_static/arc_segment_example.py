from glc import Gif
from math import pi

with Gif("arc_segment_example.gif", color_count=4) as a:
    l = a.render_list
    r = a.w // 30
    for x in range(r, a.w, r * 2):
        for y in range(r, a.h, r * 2):
            l.arcseg(
                x=x,
                y=y,
                radius=r,
                start=0,
                end=360,
                arc=90,
                line_width=10,
                phase=(x * a.w + y) * pi * 0.03
            )
