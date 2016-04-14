glc.py reference
################

.. currentmodule:: glc

Animation
~~~~~~~~~~~~~

.. autoclass:: Animation
    :members:


.. autoclass:: Gif
    :members:


.. autoclass:: ImageSequence
    :members:


Rendering
~~~~~~~~~

.. autoclass:: RenderList
    :members:


Colors
~~~~~~

.. autoclass:: glc.color.Color
    :members:

Colorspace converters
=====================

.. autofunction:: glc.color.rgb2hsv

.. autofunction:: glc.color.hsv2rgb

.. autofunction:: glc.color.rgb2hsl

.. autofunction:: glc.color.hsl2rgb

Shortcuts
=========

.. autofunction:: glc.color.rgba

.. autofunction:: glc.color.hsva

.. autofunction:: glc.color.gray

.. autofunction:: glc.color.random_rgba

.. autofunction:: glc.color.random_hsva

.. autofunction:: glc.color.random_gray

.. autofunction:: glc.color.name2color

.. autofunction:: glc.color.str2color

.. autofunction:: glc.color.int2color

.. autofunction:: glc.color.sinebow

.. autofunction:: glc.color.hue_split

.. autofunction:: glc.color.complementaries

.. autofunction:: glc.color.split_complementaries

.. autofunction:: glc.color.triads

.. autofunction:: glc.color.tetrads

.. autofunction:: glc.color.pentads

.. autofunction:: glc.color.hexads

Misc.
=====

.. autofunction:: glc.color.clerp

.. autofunction:: glc.color.multi_clerp


Utilities
~~~~~~~~~

.. autofunction:: glc.utils.deg

.. autofunction:: glc.utils.rad

.. autofunction:: glc.utils.randrange

.. autofunction:: glc.utils.clamp

.. autofunction:: glc.utils.norm

.. autofunction:: glc.utils.remap

.. autofunction:: glc.utils.lerp

.. autofunction:: glc.utils.bezier

.. autofunction:: glc.utils.quadratic

.. autofunction:: glc.utils.catmull_rom

.. autofunction:: glc.utils.spline

.. autofunction:: glc.utils.hermite

.. autofunction:: glc.utils.cosine

.. autofunction:: glc.utils.smoothstep

.. autofunction:: glc.utils.smootherstep

.. autofunction:: glc.utils.quantize

.. autofunction:: glc.utils.distribute

.. autofunction:: glc.utils.pick_closest

.. autofunction:: glc.utils.bgra_to_rgba

.. autofunction:: glc.utils.draw_image

.. autofunction:: glc.utils.quadratic_curve_to

.. autofunction:: glc.utils.curve_path

.. autofunction:: glc.utils.arc_to
