from math import sin, pi, cos
from example_util import get_filename
from glc import Gif
from glc.utils import rad
from glc.color import Color, sinebow


with Gif(get_filename(__file__), color_count=128) as a:
    a.set_bg_color(Color("black")).set_duration(5).set_size(300, 500)
    l = a.render_list
    res = 300
    phase_shift = rad(40)
    c = [sinebow(i / 2, 0.3, 0.3, 0.3, 0, 1 * phase_shift, 2 * phase_shift) for i in range(res)]
    for y in range(res - 1, 0, -4):
        l.rect(
            x=a.w * 0.5,
            y=y + 100,
            w=100 + cos(y / res * 2 * pi) * 50,
            h=100 + sin(y / res * 2 * pi) * 50,
            fill=c[y],
            stroke=Color("0x30000000"),
            line_width=4,
            scale_y=0.5,
            rotation=[0, 360],
            phase=y / res * 0.1
        )
