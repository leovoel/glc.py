from example_util import get_filename
from glc import Gif


with Gif(get_filename(__file__), emoji_path="../../dev/72x72/", save_single=0.0) as a:
    a.set_size(600, 200).set_bg_color(0xff36393e)
    l = a.render_list
    l.text(family="Comic Sans MS", x=a.w * 0.5, y=a.h * 0.5, text="this is just a single image \N{OK HAND SIGN}", fill=0xffffffff, size=40)
