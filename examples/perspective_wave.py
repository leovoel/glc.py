from example_util import get_filename
from glc.utils import remap, rad
from glc.color import rgba, sinebow
from glc.animation import Gif


with Gif(get_filename(__file__)) as a:
    l = a.render_list
    a.set_bg_color(rgba(0, 0, 0))

    fl = 250
    xc = 250
    yc = 200
    res = 20
    phase_shift = rad(60)

    for z in range(a.h + res, 0, -res):
        for x in range(a.w + res * 2, 0, -res):
            y = 50
            scale = fl / (fl + z)
            xpos = (x - 300) * scale + xc
            ypos = [(y + 50) * scale + yc, (y + 100) * scale + yc, (y + 200) * scale + yc]
            l.circle(
                x=xpos,
                y=ypos,
                radius=20 * (scale * 0.5),
                fill=sinebow(z / 10, 0.3, 0.3, 0.3, 0, 1 * phase_shift, 2 * phase_shift),
                phase=(x * 0.001) + (z * 0.001)
            )
