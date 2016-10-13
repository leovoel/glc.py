"""

    glc.image_seq
    =============

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .animation import Animation

import os
import imageio


class ImageSequence(Animation):

    """Animation rendered to a sequence of image files.

    This is a subclass of :class:`Animation`.

    Parameters
    ----------
    filename_pattern : str
        Format string that specifies what path should the images
        be saved in.

        Values passed to this format string:

        - frame
            Frame index. Generally a good idea to pad it with zeroes,
            i.e. ``'thing_{frame:04d}.png'``
    converter : str
        The converter to use. Right now, there's one converter:
        - ``'imageio'``

        Defaults to ``'imageio'``.
    """

    def __init__(self, filename_pattern, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filename_pattern = filename_pattern

        # for imageio
        _, self.format = os.path.splitext(self.filename_pattern)
        if not self.format: self.format = 'png'

        self.converter = kwargs.get('converter', 'imageio')

    def save(self):
        """Saves this animation to disk as a sequence of image files.

        Returns
        -------
        List with the paths of the generated files.
        """
        paths = []
        frames = self.render()
        func_name = 'save_with_%s' % self.converter.lower()
        func = getattr(self, func_name, self.save_with_imageio)

        for index, frame in enumerate(frames):
            path = self.filename_pattern.format(frame=index)

            with open(path, 'wb') as f:
                f.write(func(frame))

            paths.append(os.path.abspath(path))

        return paths

    def save_with_imageio(self, frame):
        """Encodes the given frame to an image file using imageio.

        Parameters
        ----------
        frame : numpy array
            Frame to encode

        Returns
        -------
        Image file as bytes
        """
        return imageio.imwrite(
            uri='<bytes>',
            im=frame,
            format=self.format
        )
