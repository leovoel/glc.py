from math import sin, pi
from example_util import get_filename
from glc import Gif


with Gif(get_filename(__file__)) as a:
    l = a.set_duration(1).set_size(300, 300).set_loop().set_ease("linear").render_list
    w = a.w // 10
    h = a.h // 10
    lw = 2
    for y in range(0, a.h, h):
        for x in range(-w * 2, a.w + w * 2, w + w):
            l.rect(
                x=x + w * 0.5 + sin(((y - h) * 2.6 / a.h) * 2 * pi) * 20 + 20,
                y=y + h * 0.5,
                w=h, h=h,
                fill="black", stroke="grey",
                line_width=lw,
                translation_x=[-w, w]
            )
        l.line(x0=0, y0=y, x1=a.w, y1=y, stroke="grey", line_width=lw)
