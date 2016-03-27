"""

    glc.config
    ==========

    At the moment this only houses the environmental variable
    for the ImageMagick binary. If you don't want to set that,
    or can't for some reason, you can replace ``None`` with the
    path where the ``convert`` application that comes with it
    lives in.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

import os


IMAGEMAGICK_BINARY = os.getenv("IMAGEMAGICK_BINARY", None)
