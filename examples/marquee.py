from example_util import get_filename
from glc import Gif


with Gif(get_filename(__file__)) as a:
    a.set_ease("linear").set_loop(False).set_duration(8).set_size(400, 100)
    l = a.render_list
    t = l.text(
        x=a.w * 0.5, y=a.h * 0.5,
        family="Comic Sans MS",
        size=30,
        text="this is text",
        translation_y=0,
    )

    ex = t.get_extents(a.context)
    t.set_prop(translation_x=[ex['text_width'] * 2, ex['text_width'] * -2])
