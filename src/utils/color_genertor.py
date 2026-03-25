def rgb(r, g, b):
    return 255 << 24 | r << 16 | g << 8 | b

def rgba(r, g, b, a):
    o = int(a * 255)
    return o << 24 | r << 16 | g << 8 | b

