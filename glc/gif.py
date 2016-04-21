"""

    glc.gif
    =============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from subprocess import Popen, DEVNULL, PIPE
from .config import IMAGEMAGICK_BINARY, FFMPEG_BINARY
from .animation import Animation
from io import IOBase

import os
import shlex
import imageio


class Gif(Animation):

    """Animation rendered to a gif file.

    This is a subclass of :class:`Animation`.

    Parameters
    ----------
    color_count : int
        Power of two value that indicates the size of the palette for the gif.
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
        Dictionary with options for the converters.
    """

    def __init__(self, filename, *args, **kwargs):
        super().__init__(filename, *args, **kwargs)
        self.color_count = kwargs.get("color_count", 256)
        self.converter = kwargs.get("converter", "imageio")
        self.converter_opts = kwargs.get("converter_opts", dict())

    def set_converter_opts(self, **kwargs):
        """Sets the options for the current converter."""
        self.converter_opts.update(kwargs)
        return self

    def save_with_imagemagick_tempfiles(self, frames, filename):
        """Writes this animation to a GIF file using ImageMagick, using temporary files.

        This exporter supports transparent backgrounds.
        This saves every frame to a temporary file.

        Parameters
        ----------
        frames : list of numpy arrays
            Container with the frames necessary to render this animation to a file.
        filename : str or file-like object
            The filename to use when saving the file.
            Can also be a file-like object.
        """
        # this is stupid

        save_as_bytes = "GIF:-"
        
        if isinstance(filename, IOBase):
            _filename = save_as_bytes
            _name = "FILE-LIKE"
        else:
            _filename = filename
            _name, _ = os.path.splitext(filename)

        temp_filenames = []

        index = 0

        for frame in frames:
            temp_name = "{}_TEMP_{:04d}.png".format(_name, index)
            temp_filenames.append(temp_name)
            imageio.imsave(temp_name, frame)
            index += 1

        delay = int(100 / self.fps)
        fuzz = self.converter_opts.get("fuzz", 1)
        layer_opt = self.converter_opts.get("layer_opt", "OptimizeTransparency")

        cmd = [
            IMAGEMAGICK_BINARY,
            "-delay", str(delay),
            "-dispose", "{:d}".format(2 if self.converter_opts.get("dispose", False) or self.transparent else 1),
            "-loop", "{:d}".format(self.converter_opts.get("loop", 0)),
            "{}_TEMP_*.png".format(_name),
            "-coalesce",
            "-layers", layer_opt,
            "-colors", str(self.color_count),
            "-fuzz", "{:02d}%".format(fuzz),
            _filename
        ]

        proc = Popen(cmd, stdout=PIPE)
        out, err = proc.communicate()

        if _filename == save_as_bytes:
            filename.write(out)
        else:
            with open(filename, "wb") as f:
                f.write(out)

        for f in temp_filenames:
            os.remove(f)

    def save_with_imagemagick(self, frames, filename):
        """Writes this animation to a GIF file using ImageMagick and FFmpeg.

        This exporter supports transparent backgrounds.
        This uses piping to avoid temporary files.

        Parameters
        ----------
        frames : list of numpy arrays
            Container with the frames necessary to render this animation to a file.
        filename : str or file-like object
            The filename to use when saving the file.
            Can also be a file-like object.
        """

        save_as_bytes = "GIF:-"
        
        if isinstance(filename, IOBase):
            _filename = save_as_bytes
        else:
            _filename = filename

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
        im_command.extend(["-", "-coalesce", _filename])

        popen_kwargs["stdin"] = ffmpeg_process.stdout
        popen_kwargs["stdout"] = PIPE
        im_process = Popen(im_command, **popen_kwargs)

        for frame in frames:
            ffmpeg_process.stdin.write(frame.tostring())

        ffmpeg_process.stdin.close()
        ffmpeg_process.wait()

        out, err = im_process.communicate()

        if _filename == save_as_bytes:
            filename.write(out)
            return

        with open(filename, "wb") as f:
            f.write(out)

    def save_with_imageio(self, frames, filename):
        """Writes this animation to a GIF file using imageio.

        This exporter does not support transparent backgrounds.

        Parameters
        ----------
        frames : list of numpy arrays
            Container with the frames necessary to render this animation to a file.
        filename : str or file-like object
            The filename to use when saving the file.
            Can also be a file-like object.
        """
        # TODO: make this more customizable

        quant = self.converter_opts.get("quantizer", "wu")

        # always get the returned bytes
        # then open, if necessary and
        # write to a file-like object

        buf = imageio.mimwrite(
            "<bytes>",
            ims=frames,
            format="gif",
            duration=1 / self.fps,
            quantizer=quant,
            palettesize=self.color_count
        )

        if isinstance(filename, IOBase):
            filename.write(buf)
        else:
            with open(filename, "wb") as f:
                f.write(buf)

    def render_and_save(self, filename=None):
        """Renders the animation and writes it to a GIF file.

        This uses the currently set exporter based on the attribute ``converter``.
        If ``converter`` is somehow ``None``, or some unknown value, the default
        is to export the animation using imageio.

        Parameters
        ----------
        filename : str
            The filename to use when saving the file.
        """
        if filename is None:
            filename = self.filename

        frames = self.render_all()
        func = getattr(self, "save_with_{}".format(self.converter), None)

        if func is None:
            self.save_with_imageio(frames, filename)
            return
        func(frames, filename)
