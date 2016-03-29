"""

    glc.animation
    =============

    Abstract definition for Animation objects.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .render_list import RenderList


class Animation:

    """Base class for animations.

    Shouldn't be instantiated. You should instead use :class:`GifAnimation`.

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

        self.set_default_style("bg_color", color)
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

    @property
    def w(self):
        return self.width

    @property
    def h(self):
        return self.height

    # context management

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if not exception_type:
            self.render_and_save(self.filename)
