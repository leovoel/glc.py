from glc import Gif
from random import randint

with Gif("curve_path_example.gif", color_count=4) as a:
    a.set_duration(2)
    l = a.render_list
    step = a.h // 25
    path0, path1 = [], []
    for x in range(0, a.w, step):
        path0.append([x, randint(0, a.h)])
        path1.append([x, randint(0, a.h)])
    l.curve_path(points=[path0, path1])
