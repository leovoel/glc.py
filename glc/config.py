"""

    glc.config
    ==========

    The two variables here define where to look for the
    ffmpeg and ImageMagick's convert binaries.
    You can either set environmental variables with the names
    FFMPEG_BINARY and IMAGEMAGICK_BINARY and point them to
    the proper files, or simply change the defaults here,
    which are ``"ffmpeg"`` and ``"convert"``.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

import os


FFMPEG_BINARY = os.getenv("FFMPEG_BINARY", "ffmpeg")
IMAGEMAGICK_BINARY = os.getenv("IMAGEMAGICK_BINARY", "convert")
