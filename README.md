# glc.py

This is a Python library made to help with the creation of code-based animation.
Heavily based on (honestly, it could be considered a "port" of) [gifloopcoder][glc] by [bit101][kp].

This uses [pycairo][pyc] for drawing. You can also use [cairocffi][ccf], which is mostly compatible with [pycairo][pyc].
To do so, add the following at the top of your script:

```py
try:
    import cairocffi
    cairocffi.install_as_pycairo()
    print("using cairocffi")
except ImportError:
    print("using pycairo")
```

## Installing

As this library is not on PyPI, you'll need to do something like:

```
pip install git+https://github.com/leovoel/glc.py
```

## Tiny Example

```py
import glc

with glc.animation.Gif("a_circle.gif", w=500, h=500) as a:
    l, w, h = a.renderlist, a.w, a.h
    l.circle(x=w * 0.5, y=h * 0.5, radius=[100, 200])
```

## Requirements

- [pycairo][pyc]/[cairocffi][ccf]
- [imageio][iio]
- [Pillow][pil]
- [numpy][npy]
- [Python 3+][py]

Normally, `pycairo`, `imageio`, `Pillow` and `numpy` should be installed when you use `pip` to install the lib.

If you want to have support for transparent gif exporting, you'll need to install [ImageMagick][imck].
After installing it, set the `IMAGEMAGICK_BINARY` environmental variable to point to the `convert` application that is part of ImageMagick.

On Windows, it's usually something like this:

```
C:\Program Files\ImageMagick-VERSION_NUMBER\convert.exe
```

To specify what converter should be used, pass `converter="imagemagick"` or `converter="imageio"`
in the constructor for a `Gif`, like so:

```py
with Gif("hey.gif", converter="imageio") as a:
    ...
```

The default is to use imageio.

[py]: https://www.python.org/
[glc]: https://github.com/bit101/gifloopcoder/
[kp]: https://github.com/bit101/
[pyc]: http://www.cairographics.org/pycairo/
[ccf]: https://github.com/SimonSapin/cairocffi
[imck]: http://imagemagick.org/script/index.php
[iio]: https://github.com/imageio/imageio
[pil]: https://github.com/python-pillow/Pillow
[npy]: http://www.numpy.org/
