from math import cos, sin, pi
from example_util import get_filename
from glc import Gif


def draw(l, surf, ctx, t):
    xpos = cos(t * 2 * pi) * 100 + surf.get_width() * 0.5
    ypos = sin(t * 2 * pi) * 100 + surf.get_height() * 0.5
    w, h = 100, 100

    ctx.set_source_rgb(0, 0, 0)
    ctx.translate(xpos, ypos)
    ctx.translate(-w * 0.5, -h * 0.5)
    ctx.rectangle(0, 0, w, w)
    ctx.fill()


Gif(get_filename(__file__), after_render=draw).render_and_save()
