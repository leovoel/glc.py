from glc import Gif
from glc.utils import lerp

with Gif("curve_example.gif", color_count=4) as a:
    a.set_duration(2)
    l = a.render_list
    wave = 100
    res = 20
    for y in range(res, a.h, res):
        l.curve(
            x0=10,
            y0=a.h * 0.5,
            x1=lerp(0.5, 10, a.h - 10),
            y1=[y + wave, y - wave],
            x2=lerp(1, 10, a.h - 10),
            y2=a.h * 0.5,
            line_width=4,
            phase=y / a.h
        )
