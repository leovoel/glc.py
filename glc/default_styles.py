"""

    glc.default_styles
    ==================

    Default styling for shapes.

    (c) 2016 LeoV
    https://github.com/leovoel/

"""

from .color import gray

import cairo


DEFAULT_STYLES = {
    "line_width": 1,
    "bg_color": gray(1.0),
    "fill": gray(0.0),
    "stroke": gray(0.0),
    "line_cap": cairo.LINE_CAP_ROUND,
    "line_dash": [],
    "line_dash_offset": 0,
    "line_join": cairo.LINE_JOIN_ROUND,
    "miter_limit": 10,
    "translation_x": 0,
    "translation_y": 0,
    "shake": 0,
    "operator": cairo.OPERATOR_OVER
}
