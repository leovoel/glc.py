from example_util import get_filename
from glc.animation import Gif
from glc.color import Color, hsva


with Gif(get_filename(__file__), converter="imageio") as a:
    a.set_bg_color(Color("black")).set_duration(2).set_size(300, 300)
    l = a.render_list
    res = 250
    c = [hsva((i / res) * 360, 1, 1) for i in range(res)]
    l.gradient_pie(x=a.w * 0.5, y=a.h * 0.5, rotation=[0, 90], rx=a.w * 0.5, ry=a.h * 0.5, colors=c)
