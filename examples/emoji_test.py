from example_util import get_filename
from glc import Gif


with Gif(get_filename(__file__), emoji_path="../../dev/72x72/") as a:
    a.set_ease("linear").set_loop(False).set_duration(5).set_size(400, 100).set_bg_color("0xff000000")
    l = a.render_list
    t = l.text(
        x=a.w * 0.5, y=a.h * 0.5,
        family="Arial",
        size=50,
        text="test 👍 test 👍👍 👍",
        translation_y=0,
        fill="0xffffdea0"
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
