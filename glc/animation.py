"""

    glc.animation
    =============

    Abstract definition for Animation objects.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .render_list import RenderList

import imageio


class Animation:

    """Base class for animations.

    Shouldn't be instantiated for the most part.
    You should instead use :class:`Gif`, unless you just want a single frame.

    Parameters
    ----------
    width : int
        Width of the drawing surface, in pixels. Defaults to 500.
    height : int
        Height of the drawing surface, in pixels. Defaults to 500.
    duration : float
        Duration of the animation, in seconds. Defaults to 2.
    fps : float
        The frame rate of the animation. Defaults to 30.
    ease : string
        The overall easing function of the animation. Defaults to ``'sine'``.
    loop : bool
        Whether the animation should loop. Defaults to ``True``.

    Attributes
    ----------
    render_list : :class:`RenderList`
        List of renderables/shapes. It's what you use to create the actual animation.
    """

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename

        self.render_list = RenderList(*args, **kwargs)
        self.width = self.render_list.width
        self.height = self.render_list.height

        self.ease = self.render_list.ease
        self.loop = self.render_list.loop

        self.duration = kwargs.pop("duration", 2.0)
        self.fps = kwargs.pop("fps", 30)

        self.save_single = kwargs.pop("save_single", None)

        self.transparent = False

    def set_size(self, width, height):
        """Changes the size of the drawing surface.

        Please note that this creates an entirely new drawing surface/context.

        Parameters
        ----------
        width : int
            New width of the surface.
        height : int
            New height of the surface.

        Returns
        -------
        self : :class:`Animation`
            For method chaining.
        """

        self.width = width
        self.height = height
        self.render_list.size(width, height)
        return self

    def set_ease(self, ease):
        """Sets the overall easing function for this animation.

        Parameters
        ----------
        ease : str
            The easing function to use.

        Returns
        -------
        self : :class:`Animation`
            For method chaining.
        """

        self.ease = ease
        self.render_list.ease = ease
        return self

    def set_loop(self, loop=None):
        """Sets the looping mode to the specified value.

        If a value for ``loop`` is not passed in, then the loop
        value is toggled - as in, if it's ``False``, then
        it will become ``True``. And vice-versa.

        Parameters
        ----------
        loop : bool
            Whether the animation should loop or not.

        Returns
        -------
        self : :class:`Animation`
            For method chaining.
        """
        if loop is None:
            self.loop = self.render_list.loop = not self.loop
        else:
            self.loop = loop
            self.render_list.loop = loop
        return self

    def set_fps(self, fps):
        """Sets the frame rate for this animation.

        Parameters
        ----------
        fps : float
            The frame rate to apply.

        Returns
        -------
        self : :class:`Animation`
            For method chaining.
        """

        self.fps = fps
        self.render_list.fps = fps
        return self

    def set_duration(self, duration):
        """Sets the duration for this animation.

        Parameters
        ----------
        duration : float
            The duration to apply.

        Returns
        -------
        self : :class:`Animation`
            For method chaining.
        """

        self.duration = duration
        self.render_list.duration = duration
        return self

    def set_default_style(self, name, value):
        """Sets a default style to the specified value.

        Parameters
        ----------
        name : str
            The name of the style attribute to change.
        value : str
            The value to apply.

        Returns
        -------
        self : :class:`Animation`
            For method chaining.
        """

        if name in self.render_list.default_styles:
            self.render_list.default_styles[name] = value
        return self

    def set_bg_color(self, color):
        """Shortcut to set the background color to the specified color.

        See the documentation on colors to know what kind of
        value you should pass as a parameter to this function.

        Parameters
        ----------
        color : :class:`Color`
            The color to use in the background.

        Returns
        -------
        self : :class:`Animation`
            For method chaining.
        """
        if isinstance(color, str):
            if color.lower() == "transparent":
                self.transparent = True
            else:
                self.transparent = False
        self.set_default_style("bg_color", color)
        return self

    def set_emoji_path(self, path):
        """Defines where the library will try to find emoji images.

        The library expects a folder with organization (and filenames)
        similar to the ones you can get from twemoji, like this:
        https://github.com/twitter/twemoji/tree/gh-pages/72x72

        Parameters
        ----------
        path : str
            The path to the folder containing the emoji images.

        Returns
        -------
        self : :class:`Animation`
            For method chaining.
        """
        self.render_list.emoji_path = path
        return self

    def render_all(self):
        """Renders all the necessary frames for this animation to numpy arrays.

        Returns
        -------
        frames : list of numpy arrays
        """
        frames = []

        total_frames = self.duration * self.fps
        speed = 1 / total_frames
        t = 0
        rendering = True

        while rendering:
            frames.append(self.render_list.render(t))
            t += speed
            if round(t * 10000) / 10000 >= 1:
                t = 0
                rendering = False

        return frames

    def render_one(self, t, filename=None):
        """Renders one frame at time t then export it to a file.

        If filename is ``"<bytes>"``, then the frame is returned as a numpy array.

        Parameters
        ----------
        t : float
            The time to render at.
            Should be a value within the range 0.0 to 1.0.
        filename : str
            The path + name of the file + extension to save the image in.

        Returns
        -------
        The rendered frame as a numpy array.
        """
        if filename is None:
            filename = self.filename

        frame = self.render_list.render(t)

        if filename is not "<bytes>":
            imageio.imwrite(filename, frame)
            return
        return frame

    @property
    def context(self):
        """Shortcut to access the Cairo context of the render list for this animation."""
        return self.render_list.context

    @property
    def w(self):
        """Shortcut to access the width of the animation."""
        return self.width

    @property
    def h(self):
        """Shortcut to access the height of the animation."""
        return self.height

    # context management

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if not exception_type:
            if self.save_single is not None:
                self.render_one(self.save_single)
                return
            self.render_and_save()
