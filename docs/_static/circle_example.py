from math import sqrt
from glc import Gif

with Gif("circle_example.gif", color_count=4) as a:
    a.set_duration(2)
    l = a.render_list
    r = a.w // 50
    cx, cy = a.w * 0.5, a.h * 0.5
    for x in range(r * 2, a.w - r, r * 2):
        for y in range(r * 2, a.h - r, r * 2):
            dx = x - cx
            dy = y - cy
            dist = sqrt(dx * dx + dy * dy)
            l.circle(
                x=x, y=y,
                radius=r,
                phase=dist * 0.003,
                line_width=2,
                start=0, end=[0, 360],
                centered=True
            )
