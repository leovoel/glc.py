from example_util import get_filename
from glc import Gif
from glc.color import sinebow
from glc.utils import rad


with Gif(get_filename(__file__)) as a:
    l = a.render_list

    tw = 60
    th = tw * 0.5

    ps = rad(60)

    for y in range(40):
        for x in range(40):
            xpos = a.w * 0.5 + (x - y) * tw * 0.5
            ypos = -tw * 2 + (x + y) * th * 0.5
            l.isobox(
                x=xpos,
                y=ypos,
                size=tw,
                h=[-10, 100],
                phase=(x * y) * 0.002,
                color_top=sinebow(x + y * 0.2, 0.3, 0.3, 0.3, 0 * ps, 1 * ps, 2 * ps),
                color_left=sinebow(x + y * 0.2, 0.3, 0.3, 0.3, 0 * ps, 1 * ps, 2 * ps).darken(10),
                color_right=sinebow(x + y * 0.2, 0.3, 0.3, 0.3, 0 * ps, 1 * ps, 2 * ps).darken(20)
            )

    a.save()
