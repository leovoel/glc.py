from glc import Gif

with Gif("arrow_example.gif", color_count=4) as a:
    l = a.render_list
    n = 20
    w, h = a.w // n, a.h // n
    for x in range(w // 2, a.w, w):
        for y in range(h // 2, a.h, h):
            l.arrow(
                x=x,
                y=y,
                w=[w, w * 1.5],
                h=[h, h * 1.5],
                rotation=[0, 180],
                phase=((x + 300) * y) / (a.w * a.h)
            )
