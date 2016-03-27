from example_util import get_filename
from glc.animation import Gif


with Gif(get_filename(__file__), converter="imageio") as a:
    a.set_ease("back").set_duration(2)
    l = a.render_list
    for x in range(100, a.w, 150):
        for y in range(50, a.h - 50, 70):
            l.text(
                x=x, y=y,
                family="SimHei",
                size=50,
                text="(>o_o)>,<(o_o<),\(-O-)/ ".split(","),
                translation_y=[0, 10],
                rotation=[-10, 0, 10],
                phase=(x + y) * 0.00345
            )
