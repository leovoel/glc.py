"""

    glc.gif
    =============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from subprocess import Popen, DEVNULL, PIPE
from .config import IMAGEMAGICK_BINARY, FFMPEG_BINARY
from .animation import Animation
from .utils import clamp
from io import IOBase

import os
import shlex
import imageio


class Gif(Animation):

    """Animation rendered to a gif file.

    This is a subclass of :class:`Animation`.

    Parameters
    ----------
    filename : str or file-like object
        Where to save this GIF.
    color_count : int
        GIF palette size, should be a power of two, and in the 2-256 range.
        Defaults to 256.
    converter : str
        The converter to use. Right now, there are three converters:
        - ``'imagemagick'``
        - ``'imagemagick_tempfiles'``
        - ``'imageio'``

        The ``imagemagick[_tempfiles]`` converters are the
        only ones that support transparent gifs.

        Defaults to ``'imageio'``.
    converter_opts : dict
        Dictionary with extra options for the converters.
    """

    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filename = filename

        self.color_count = kwargs.get("color_count", 256)

        # TODO: document extra converter options
        self.converter = kwargs.get("converter", "imageio")
        self.converter_opts = kwargs.get("converter_opts", dict())

    def set_converter_opts(self, **kwargs):
        """Sets the options for the current converter."""
        self.converter_opts.update(kwargs)
        return self

    def save(self):
        """Writes this animation to a GIF file.

        Uses the specified converter, unless that doesn't exist,
        in which case imageio is the default.
        """
        # TODO: add warning about this?
        if self.color_count not in (2, 4, 8, 16, 32, 64, 128, 256):
            self.color_count = 1 << (clamp(self.color_count, 2, 256) - 1).bit_length()

        frames = self.render()

        func_name = "save_with_%s" % self.converter.lower()
        func = getattr(self, func_name, self.save_with_imageio)
        result = func(frames)

        if isinstance(self.filename, IOBase):
            self.filename.write(result)
        else:
            with open(self.filename, "wb") as f:
                f.write(result)

    def save_with_imagemagick_tempfiles(self, frames):
        """Writes this animation to a GIF file using ImageMagick, using temporary files.

        This converter supports transparent backgrounds.
        This saves every frame to a temporary file.

        Parameters
        ----------
        frames : list of numpy arrays
            Container with the frames necessary to render this animation to a file.

        Returns
        -------
        Image file as bytes
        """
        # this is stupid

        # TODO: append random string?
        filename = "GLC_ANIM"

        temp_filenames = []

        for index, frame in enumerate(frames):
            temp_name = "{}_TEMP_{:04d}.png".format(filename, index)
            temp_filenames.append(temp_name)
            imageio.imsave(temp_name, frame)

        delay = int(100 / self.fps)
        fuzz = self.converter_opts.get("fuzz", 1)
        layer_opt = self.converter_opts.get("layer_opt", "OptimizeTransparency")

        cmd = [
            IMAGEMAGICK_BINARY,
            "-delay", str(delay),
            "-dispose", "{:d}".format(2 if self.converter_opts.get("dispose", False) or self.transparent else 1),
            "-loop", "{:d}".format(self.converter_opts.get("loop", 0)),
            "{}_TEMP_*.png".format(filename),
            "-coalesce",
            "-layers", layer_opt,
            "-colors", str(self.color_count),
            "-fuzz", "{:02d}%".format(fuzz),
            "GIF:-"
        ]

        proc = Popen(cmd, stdout=PIPE)
        out, err = proc.communicate()

        for f in temp_filenames:
            os.remove(f)

        return out

    def save_with_imagemagick(self, frames):
        """Writes this animation to a GIF file using ImageMagick and FFmpeg.

        This converter supports transparent backgrounds.
        This uses piping to avoid temporary files.

        Parameters
        ----------
        frames : list of numpy arrays
            Container with the frames necessary to render this animation to a file.

        Returns
        -------
        Image file as bytes
        """

        # NOTE: main idea here is to grab frames using ffmpeg,
        # and pipe those to imagemagick's convert.
        # the reason we don't just use ffmpeg is because
        # it produces incredibly grainy gifs by default,
        # and most people on the web say that the best way is
        # to use imagemagick *shrugs*
        # this is based on moviepy's gif writers
        # (https://github.com/Zulko/moviepy/blob/master/moviepy/video/io/gif_writers.py)
        # thanks!

        delay = 100.0 / self.fps

        # NOTE: for the last -vcodec, ppm or bmp works, png doesn't???
        # ppm is fine for non transparent stuff,
        # otherwise bmp is the one that works properly.
        # see also: http://www.ffmpeg.org/general.html#toc-Image-Formats

        ffmpeg_command = [
            FFMPEG_BINARY,
            "-y",
            "-loglevel", "error",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-r", "{:.02f}".format(self.fps),
            "-s", "{:d}x{:d}".format(self.w, self.h),
            "-pix_fmt", "rgba",
            "-i", "-",
            "-f", "image2pipe",
            "-vcodec", ("bmp" if self.transparent else "ppm"),
            "-"
        ]

        popen_kwargs = {"stdout": DEVNULL, "stderr": DEVNULL, "stdin": DEVNULL}

        # NOTE: CREATE_NO_WINDOW
        # see https://msdn.microsoft.com/en-us/library/windows/desktop/ms684863%28v=vs.85%29.aspx
        if os.name == "nt":
            popen_kwargs["creationflags"] = 0x08000000

        popen_kwargs["stdin"] = PIPE
        popen_kwargs["stdout"] = PIPE

        ffmpeg_process = Popen(ffmpeg_command, **popen_kwargs)

        # RE: dispose
        # see http://www.imagemagick.org/script/command-line-options.php#dispose
        # we use 2 if the animation is meant to be transparent
        # otherwise you're on your own, and should set the "dispose" option
        # in the converter_opts arg in the constructor, or set_converter_opts
        im_command = [
            IMAGEMAGICK_BINARY,
            "-delay", "{:.02f}".format(delay),
            "-dispose", "{:d}".format(2 if self.converter_opts.get("dispose", False) or self.transparent else 1),
            "-loop", "{:d}".format(self.converter_opts.get("loop", 0)),
        ]

        im_command.extend(shlex.split(self.converter_opts.get("before_args", "")))
        im_command.extend(["-", "-coalesce", "GIF:-"])

        popen_kwargs["stdin"] = ffmpeg_process.stdout
        popen_kwargs["stdout"] = PIPE
        im_process = Popen(im_command, **popen_kwargs)

        for frame in frames:
            ffmpeg_process.stdin.write(frame.tostring())

        ffmpeg_process.stdin.close()
        ffmpeg_process.wait()

        out, err = im_process.communicate()

        return out

    def save_with_imageio(self, frames):
        """Writes this animation to a GIF file using imageio.

        This converter does not support transparent backgrounds.

        Parameters
        ----------
        frames : list of numpy arrays
            Container with the frames necessary to render this animation to a file.

        Returns
        -------
        Image file as bytes
        """
        return imageio.mimwrite(
            "<bytes>",
            ims=frames,
            format="gif",
            duration=1 / self.fps,
            quantizer=self.converter_opts.get("quantizer", "wu"),
            palettesize=self.color_count
        )
