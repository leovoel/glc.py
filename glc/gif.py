"""

    glc.gif
    =============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .config import IMAGEMAGICK_BINARY
from .animation import Animation

import os
import subprocess
import imageio


class Gif(Animation):

    """Animation rendered to a gif file.

    Parameters
    ----------
    color_count : int
        Power of two value that indicates the size of the palette for the gif.
        Defaults to 256.
    converter : str
        The converter to use. Right now, there are two converters:
        - ``'imagemagick'``
        - ``'imageio'``

        The ``imagemagick`` converter is the only one that supports
        transparent gifs, but it uses temporary files, which is
        not very clean.

        Defaults to ``'imageio'``.
    convert_opts : dict
        Dictionary with options for the converters.
    """

    def __init__(self, filename, *args, **kwargs):
        super().__init__(filename, *args, **kwargs)
        self.color_count = kwargs.get("color_count", 256)
        self.converter = kwargs.get("converter", "imageio")
        self.convert_opts = kwargs.get("convert_opts", dict())

    def save_with_imagemagick(self, frames, filename):
        # this is stupid
        # but it's the only way we can have transparent gifs
        # TODO: make this more customizable

        _filename, _file_extension = os.path.splitext(filename)

        temp_filenames = []

        index = 0

        for frame in frames:
            temp_name = "{}_TEMP_{:04d}.png".format(_filename, index)
            temp_filenames.append(temp_name)
            imageio.imsave(temp_name, frame)
            index += 1

        delay = int(100 / self.fps)
        fuzz = self.convert_opts.get("fuzz", 1)
        layer_opt = self.convert_opts.get("layer_opt", "OptimizeTransparency")

        cmd = [
            IMAGEMAGICK_BINARY,
            "-delay", str(delay),
            "-dispose", "2",
            "-loop", "0",
            "{}_TEMP_*.png".format(_filename),
            "-coalesce",
            "-layers", layer_opt,
            "-colors", str(self.color_count),
            "-fuzz", "{:02d}%".format(fuzz),
            filename
        ]

        proc = subprocess.Popen(cmd)
        proc.wait()

        for f in temp_filenames:
            os.remove(f)

    def save_with_imageio(self, frames, filename):
        # TODO: make this more customizable
        # TODO: add support for more formats (like videos)?

        quant = self.convert_opts.get("quantizer", "wu")

        writer = imageio.get_writer(
            filename,
            duration=1 / self.fps,
            quantizer=quant,
            palettesize=self.color_count
        )

        for frame in frames:
            writer.append_data(frame)

        writer.close()

    def render_and_save(self, filename):
        frames = self.render_all()
        getattr(self, "save_with_{}".format(self.converter))(frames, filename)
