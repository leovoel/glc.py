from math import sin, pi
from example_util import get_filename
from glc.animation import Gif
from glc.color import Color


with Gif(get_filename(__file__), converter="imageio") as a:
    a.set_size(300, 200).set_fps(50).set_ease("quartic").set_bg_color("0xff36393e")
    l = a.render_list
    l.img(x=a.w * 0.6, y=a.h * 0.5 - 20, rotation=[360, 0], img="eyes.png", translation_x=[200, 0])
    l.img(x=a.w * 0.25, y=a.h * 0.5, shake=[10, 100], img="ok.png")
