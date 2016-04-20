from example_util import get_filename
from glc import Gif
from glc.color import split_complementaries, Color


with Gif(get_filename(__file__), color_count=8) as a:
    col, col2, col3 = split_complementaries(Color("mustard"), 140)

    l = a.set_bg_color(col).set_size(400, 400).set_fps(24).set_duration(4).set_loop().set_ease("linear").render_list
    r, lw = a.w // 40, 3
    for x in range(r * 2, a.w - r, r * 2):
        for y in range(r * 2, a.h - r, r * 2):
            c = l.container(x=x, y=y, rotation=[0, 360], phase=(x + y) / a.w)
            l.oval(x=0, y=0, rx=r, ry=r * 0.5, stroke=False, fill=col3, parent=c)
            l.oval(x=0, y=0, rx=r, ry=r * 0.5, stroke="white", fill=False, start=0, end=180, line_width=lw, parent=c)
            l.oval(x=0, y=0, rx=r, ry=r * 0.5, stroke=Color(col3).darken(20), fill=False, start=180, end=360, line_width=lw, parent=c)


import os
os.startfile(get_filename(__file__))
