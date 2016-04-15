from glc import Gif

with Gif("bezier_curve_example.gif", color_count=4) as a:
    a.set_duration(2)
    l = a.render_list
    ys, s, h = 10, 10, 200
    for i in range(a.h // s):
        c = [ys + (i * s) - h, ys + (i * s) + h]
        l.bezier(
            x0=0, y0=a.h * 0.5,
            x1=a.w * 0.3, y1=c,
            x2=a.w * 0.6, y2=list(reversed(c)),
            x3=a.w, y3=a.h * 0.5,
            phase=(i * 2) / (a.h // s),
            line_width=2
        )
