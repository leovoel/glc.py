from example_util import get_filename
from glc.utils import rad
from glc.color import sinebow
from glc.animation import Gif


with Gif(get_filename(__file__)) as a:
    l = a.render_list
    a.set_bg_color("black")

    phase_shift = rad(50)
    s = 50
    res = 30

    for x in range(0, a.w, res):
        for y in range(0, a.h + s, res):
            l.rect(
                x=x,
                y=-y + a.h,
                w=[s, s * 0.2],
                h=[s, s * 0.2],
                fill=sinebow(y / 10, 0.3, 0.3, 0.3, 0, 1 * phase_shift, 2 * phase_shift),
                scale_y=0.5,
                rotation=[0, 90],
                phase=(x + y) * 0.001
            )
