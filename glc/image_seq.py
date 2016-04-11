"""

    glc.image_seq
    =============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .animation import Animation

import imageio


class ImageSequence(Animation):

    """Animation rendered to a sequence of image files.

    This is a subclass of :class:`Animation`.
    """

    def render_and_save(self, filename):
        """Renders the animation and writes it to a sequence of image files.

        Parameters
        ----------
        filename : str
            The name to use when saving the files.
        """
        frames = self.render_all()

        n = filename.split(".")

        name = "".join(n[:-1])
        ext = n[-1]

        for index, frame in enumerate(frames):
            imageio.imwrite("{0}{1:04d}.{2}".format(name, index, ext), frame)
