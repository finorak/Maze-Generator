"""Color helper functions to build ARGB integer values.

Small helpers that pack RGB(A) components into a single integer used
by the rendering code.
"""


def rgb(r: int, g: int, b: int) -> int:
    """Pack RGB into a 32-bit ARGB integer with full alpha."""
    return 255 << 24 | r << 16 | g << 8 | b


def rgba(r: int, g: int, b: int, a: int) -> int:
    """Pack RGBA into a 32-bit ARGB integer using alpha fraction.

    Args:
        r,g,b: Color channels 0-255.
        a: Alpha fraction between 0.0 and 1.0 (multiplied by 255).
    """
    o = int(a * 255)
    return o << 24 | r << 16 | g << 8 | b
