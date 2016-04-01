from example_util import get_filename
from glc import Gif


with Gif(get_filename(__file__)) as a:
    a.set_ease("linear").set_loop(False).set_duration(4).set_size(400, 100)
    l = a.render_list
    t = l.text(
        x=a.w * 0.5, y=a.h * 0.5,
        family="Comic Sans MS",
        size=30,
        text="text test text test",
        translation_y=0,
    )

    ex = t.get_extents(a.context)
    tw = ex["text_width"]

    # the proper way to put the text at the edge of the canvas is:
    # animation width / 2 + text width / 2
    # for the other way around, invert the signs, so
    # -animation width / 2 - text width / 2

    t.set_prop(
        translation_x=[a.w * 0.5 + tw * 0.5, -a.w * 0.5 - tw * 0.5]
    )
