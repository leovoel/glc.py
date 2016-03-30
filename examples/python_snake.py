from example_util import get_filename
from glc import Gif
from glc.color import Color, hue_split


with Gif(get_filename(__file__)) as a:
    l = a.set_duration(7).set_ease("elastic").set_size(300, 400).render_list

    blu = Color("0xFF3774A3")
    yel = Color("0xFFDFAD20").desaturate(10).lighten(5)

    c = l.container(x=a.w * 0.5, y=a.h * 0.5, rotation=[-180, 0], scale_x=[0.5, 1.5, 1], scale_y=[0.5, 1.5, 1])

    l.roundrect(x=0, y=0, w=140, h=120, line_width=10, radius=35, fill=yel, stroke="white", translation_x=40, translation_y=0, parent=c)

    l.roundrect(x=0, y=0, w=120, h=120, line_width=10, radius=35, fill=blu, stroke="white", translation_x=0, translation_y=-60, parent=c)

    l.roundrect(x=0, y=0, w=140, h=120, line_width=10, radius=30, fill=blu, stroke="white", translation_x=-40, parent=c)

    l.rect(x=0, y=0, translation_x=-14, translation_y=-30, w=100, h=50, stroke=False, fill=blu, parent=c)

    l.roundrect(x=0, y=0, w=120, h=120, line_width=10, radius=35, fill=yel, stroke="white", translation_x=0, translation_y=60, parent=c)

    l.rect(x=0, y=0, translation_x=30, translation_y=30, w=100, h=50, stroke=False, fill=yel, parent=c)

    l.circle(x=0, y=0, radius=[0, 10], translation_x=-30, translation_y=-90, fill="white", stroke=False, parent=c, phase=0.02).set_ease("elastic")

    l.circle(x=0, y=0, radius=[0, 10], translation_x=30, translation_y=90, fill="white", stroke=False, parent=c).set_ease("elastic")

    l.ray(x=0, y=0, translation_x=-10, translation_y=60, line_width=10, length=80, stroke="white", parent=c)
