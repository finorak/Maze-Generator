"""Lightweight image container used by maze cells.

This module defines a simple `Image` holder that stores image
handles and raw buffer metadata for integration with the mlx layer.
"""

from typing import Any


class Image:
    """Container for image handles and pixel buffer metadata."""
    def __init__(self) -> None:
        """Initialize empty image handles and mlx buffer metadata."""
        self.img: Any = None
        self.width = 0
        self.height = 0
        self.data: Any = None
        self.width = 0
        self.height = 0
        self.bpp = 0
        self.sl = 0
        self.ioformat = 0
        self.is_init = False
