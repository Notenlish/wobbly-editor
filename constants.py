from pygame import Rect
import sys
import platform

import pygame

WEB = sys.platform in ("emscripten", "wasi")

WEB_MOBILE = WEB and platform.window.mobile_check()  # type:ignore
WEB_TABLET = WEB and platform.window.mobile_tablet()  # type:ignore

SIZE = WIDTH, HEIGHT = (640, 360)

SC_TOPLEFT = pygame.Vector2(0, 0)
SC_TOPRIGHT = pygame.Vector2(WIDTH, 0)
SC_BOTTOMLEFT = pygame.Vector2(0, HEIGHT)
SC_BOTTOMRIGHT = pygame.Vector2(WIDTH, HEIGHT)

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
