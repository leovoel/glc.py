from glc import Gif
from glc.utils import lerp

with Gif("bezier_segment_example.gif", color_count=4) as a:
    a.set_duration(4)
    l = a.render_list
    start_x, start_y = -10, 10
    sw = 100
    s = 5
    end_y = a.h - start_y
    for i in range(a.w // s + 2):
        l.bezierseg(
            x0=start_x + (i * s), y0=start_y,
            x1=start_x + sw + (i * s), y1=lerp(0.3, start_y, end_y),
            x2=start_x - sw + (i * s), y2=lerp(0.6, start_y, end_y),
            x3=start_x + (i * s), y3=end_y,
            phase=i / (a.w // s),
            line_width=2
        )
