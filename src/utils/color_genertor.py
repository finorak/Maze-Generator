def rgb(r: int, g: int, b: int) -> int:
    return 255 << 24 | r << 16 | g << 8 | b


def rgba(r: int, g: int, b: int, a: int) -> int:
    o = int(a * 255)
    return o << 24 | r << 16 | g << 8 | b
