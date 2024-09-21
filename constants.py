from pygame import Rect

SIZE = WIDTH, HEIGHT = (640, 360)
PAINT_SIZE = 8
CLEAR_SIZE = 12
SCREEN_RECT = Rect(0, 0, *SIZE)

# formats supported by pygame-ce. see: https://pyga.me/docs/ref/image.html
PG_SUPPORTED_IMG_FORMATS = [
    ".bmp",
    ".gif",
    ".jpeg",
    ".jpg",
    ".lbm",
    ".pcx",
    ".png",
    ".pnm",
    ".pbm",
    ".pgm",
    ".ppm",
    ".qoi",
    ".svg",
    ".tvga",
    ".tiff",
    ".webp",
    ".xpm",
    ".xcf",
]
