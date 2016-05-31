"""

    glc.render_list
    ===============

    Drawing by adding shapes to a list.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from copy import deepcopy
from .shapes import *
from .color import Color
from .utils import bgra_to_rgba, is_emoji
from .default_styles import DEFAULT_STYLES

import os
import io
import cairo
import numpy
import imageio


class RenderList:

    """List of renderables/shapes.

    Parameters
    ----------
    width : int
        Width of the drawing surface, in pixels. Defaults to 500.
    height : int
        Height of the drawing surface, in pixels. Defaults to 500.
    default_styles : dict
        Default styling for shapes.
    ease : string
        The overall easing function of the animation. Defaults to ``'sine'``.
    loop : bool
        Whether the animation should loop. Defaults to ``True``.
    emoji_path : string
        Where the emoji pngs are located. Defaults to ``None``.
    before_render : callable
        A function that takes in this render list, a Cairo surface, context, and a time ``t``.
        It's called before all shapes are rendered.
        Defaults to ``None``.
    after_render : callable
        A function that takes in this render list, a Cairo surface, context, and a time ``t``.
        It's called after all shapes are rendered.
        Defaults to ``None``.

    Attributes
    ----------
    surface : :class:`cairo.ImageSurface`
        Memory buffer for storing drawings onto.
    context : :class:`cairo.Context`
        Drawing context.
    shapes : list of :class:`Shape`
        The list of shapes to render.
    """

    def __init__(self, *args, **kwargs):
        self.width = kwargs.pop("width", 500)
        self.height = kwargs.pop("height", 500)
        self.mem_format = cairo.FORMAT_ARGB32  # expose this?

        self.ease = kwargs.pop("ease", "sine")
        self.loop = kwargs.pop("loop", True)

        self.default_styles = deepcopy(DEFAULT_STYLES)
        self.default_styles.update(kwargs.pop("default_styles", {}))

        self.surface = cairo.ImageSurface(self.mem_format, self.width, self.height)
        self.context = cairo.Context(self.surface)

        self.emoji_path = kwargs.pop("emoji_path", None)

        self.before_render = kwargs.pop("before_render", None)
        self.after_render = kwargs.pop("after_render", None)

        self.shapes = []
        self._cached_images = {}
        self._emoji_cache = {}

    def size(self, width=500, height=500):
        """Changes the size of the surface.

        Please note that this creates an entirely new surface/context.

        Parameters
        ----------
        width : int
            New width of the surface.
        height : int
            New height of the surface.

        Returns
        -------
        (width, height) : tuple of int
        """

        self.width = width
        self.height = height

        self.surface.finish()
        self.surface = cairo.ImageSurface(self.mem_format, self.width, self.height)
        self.context = cairo.Context(self.surface)

        return width, height

    def add(self, shape):
        """Adds a shape to the list.

        Parameters
        ----------
        shape : :class:`Shape`

        Returns
        -------
        shape : :class:`Shape`
            The added shape.
        """

        if shape.ease is None:
            shape.ease = self.ease
        if shape.loop is None:
            shape.loop = self.loop

        # support for parenting
        if shape.props.get("parent", None):
            shape.props['parent'].add(shape)
        else:
            self.shapes.append(shape)

        shape.default_styles = self.default_styles

        return shape

    def render(self, t):
        """Returns an image (frame) of this render list at time t.

        Parameters
        ----------
        t : float
            Specifies at what point in time this list should be rendered in.

        Returns
        -------
        buf : array
            The frame as a numpy array.
        """

        bg = self.default_styles["bg_color"]

        self.context.save()

        # TODO: accept some other values to clear the screen?
        if bg == "transparent":
            self.context.set_source_rgba(0, 0, 0, 0)
            self.context.set_operator(cairo.OPERATOR_CLEAR)
            self.context.paint()
        else:
            self.context.set_source_rgba(*Color(bg))
            self.context.paint()

        self.context.restore()

        self.context.set_operator(cairo.OPERATOR_OVER)

        if self.before_render is not None:
            self.context.save()
            self.before_render(self, self.surface, self.context, t)
            self.context.restore()

        for shape in self.shapes:
            shape.render(self.context, t)

        if self.after_render is not None:
            self.context.save()
            self.after_render(self, self.surface, self.context, t)
            self.context.restore()

        # convert the stupid cairo surface from
        # bgra to rgba using pillow first, then
        # convert that to a numpy array
        # v silly

        buffer = bgra_to_rgba(self.surface)
        buf = numpy.frombuffer(buffer, numpy.uint8)
        buf.shape = (self.height, self.width, 4)
        return buf

    # shortcuts to add shapes
    # TODO: document shapes
    # NOTE: should this documentation be duplicated here (as docstrings on these methods)?

    def arc_segment(self, *args, **kwargs):
        return self.add(ArcSegment(*args, **kwargs))

    arcseg = arc_segment

    def arrow(self, *args, **kwargs):
        return self.add(Arrow(*args, **kwargs))

    def bezier_curve(self, *args, **kwargs):
        return self.add(BezierCurve(*args, **kwargs))

    bezier = bezier_curve

    def bezier_segment(self, *args, **kwargs):
        return self.add(BezierSegment(*args, **kwargs))

    bezierseg = bezier_segment

    def circle(self, *args, **kwargs):
        return self.add(Circle(*args, **kwargs))

    def container(self, *args, **kwargs):
        return self.add(Container(*args, **kwargs))

    def curve(self, *args, **kwargs):
        return self.add(Curve(*args, **kwargs))

    def curve_path(self, *args, **kwargs):
        return self.add(CurvePath(*args, **kwargs))

    def curve_segment(self, *args, **kwargs):
        return self.add(CurveSegment(*args, **kwargs))

    curveseg = curve_segment

    def gear(self, *args, **kwargs):
        return self.add(Gear(*args, **kwargs))

    def gradient_pie(self, *args, **kwargs):
        return self.add(GradientPie(*args, **kwargs))

    def grid(self, *args, **kwargs):
        return self.add(Grid(*args, **kwargs))

    def heart(self, *args, **kwargs):
        return self.add(Heart(*args, **kwargs))

    def image(self, *args, **kwargs):
        imgs = kwargs.get("img", None)

        if not imgs:
            return

        # TODO: make more robust
        if not isinstance(imgs, (list, tuple)):
            imgs = [imgs]

        surfaces = []
        durations = []

        for img in imgs:
            # special case for strings with one emoji

            # TODO: make this an option?

            # TODO: this fails for some cases
            # so the right thing to do here would be to abstract it out
            # into a special "get the right image" module.
            # refer to twemoji: https://github.com/twitter/twemoji
            if isinstance(img, str):
                if len(img) == 1 and is_emoji(img) and self.emoji_path:
                    hex_val = img.encode("unicode-escape").decode("ascii").lstrip("\\U0")

                    if img not in self._emoji_cache:
                        # TODO: not assume that .png is the format available
                        path = os.path.abspath(os.path.join(self.emoji_path, hex_val + ".png"))
                        surfaces.append(cairo.ImageSurface.create_from_png(path))
                else:
                    surfaces.append(self._emoji_cache[char])

                continue

            if img in self._cached_images:
                for surface in self._cached_images[img]:
                    surfaces.append(surface)
            else:
                reader = imageio.get_reader(img)

                self._cached_images[img] = []

                for index, im in enumerate(reader):

                    # get frame durations here (for gifs)
                    # U N D O C U M E N T E D  B O Y Z

                    try:
                        duration = reader._get_meta_data(index)
                        durations.append(duration["ANIMATION"]["FrameTime"])
                    except Exception:
                        pass

                    writer = imageio.imwrite("<bytes>", im, "png")
                    img_surf = cairo.ImageSurface.create_from_png(io.BytesIO(writer))
                    surfaces.append(img_surf)
                    self._cached_images[img].append(img_surf)

                reader.close()

        duration = None
        if durations:
            # in seconds
            duration = sum(durations) / 1000.0

        kwargs["image_surfaces"] = surfaces
        kwargs["duration"] = duration
        kwargs["durations"] = durations
        return self.add(Image(*args, **kwargs))

    img = image

    def isobox(self, *args, **kwargs):
        return self.add(IsoBox(*args, **kwargs))

    def isotube(self, *args, **kwargs):
        return self.add(IsoTube(*args, **kwargs))

    def line(self, *args, **kwargs):
        return self.add(Line(*args, **kwargs))

    def oval(self, *args, **kwargs):
        return self.add(Oval(*args, **kwargs))

    def path(self, *args, **kwargs):
        return self.add(Path(*args, **kwargs))

    def poly(self, *args, **kwargs):
        return self.add(Poly(*args, **kwargs))

    def ray(self, *args, **kwargs):
        return self.add(Ray(*args, **kwargs))

    def ray_segment(self, *args, **kwargs):
        return self.add(RaySegment(*args, **kwargs))

    rayseg = ray_segment

    def rect(self, *args, **kwargs):
        return self.add(Rect(*args, **kwargs))

    def roundrect(self, *args, **kwargs):
        return self.add(RoundRect(*args, **kwargs))

    def segment(self, *args, **kwargs):
        return self.add(Segment(*args, **kwargs))

    def spiral(self, *args, **kwargs):
        return self.add(Spiral(*args, **kwargs))

    def splat(self, *args, **kwargs):
        return self.add(Splat(*args, **kwargs))

    def star(self, *args, **kwargs):
        return self.add(Star(*args, **kwargs))

    def text(self, *args, **kwargs):
        kwargs["emoji_path"] = self.emoji_path
        kwargs["emoji_cache"] = self._emoji_cache
        return self.add(Text(*args, **kwargs))
