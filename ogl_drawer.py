import zengl
from typing import Literal, TypedDict, Callable
import pygame

from constants import SIZE
from ogl_draw_funcs import draw_circle

type DrawColor = str | tuple[int, int, int] | pygame.Color
type DrawRadius = float | int
type DrawOutlineWidth = int

type DrawOptions = Literal["circle"]
# I just realized something, instead of doing nested dicts, I could, just, use a single tuple.
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# TODO: simplify this to just use a tuple

type DrawCircleCache = dict[
    DrawColor, dict[DrawRadius, dict[DrawOutlineWidth, zengl.Image]]
]

# what the actual fuck am I doing
type DrawTypes = Literal["circle"]

type DrawOptionToFunction = dict[DrawOptions, Callable[..., pygame.Surface]]


class DrawCache(TypedDict):
    circle: DrawCircleCache


class OpenGLDrawer:
    def __init__(self, ctx: zengl.Context) -> None:
        self.ctx = ctx
        self.func_to_type: DrawOptionToFunction = {"circle": draw_circle}
        self.__init_caches()

    def __init_caches(self):
        self.cache = {"circle": {}}

    def draw_circle(
        self,
        img_to_draw: zengl.Image,
        pos: tuple[int, int] | list[int],
        color: DrawColor,
        radius: DrawRadius,
        outline: DrawOutlineWidth,
    ):
        pos = list(pos)
        pos[1] = SIZE[1] - pos[1]
        # offset = pos[0] + pos[1] * img_to_draw.size[0]
        img = self.get_cache_or_draw("circle", color, radius, outline)
        img.blit(img_to_draw, pos, img.size)

    def get_cache_or_draw(self, type_: DrawTypes, *args) -> zengl.Image:
        # What does this do?
        # Basically, this is a cache system that caches the outputs of pygame.draw functions.
        # Since each draw function has a different amount/type of args, it uses recursion
        # It iteratively goes through every arg given, until it finds the last arg
        # if an cache hasnt been initted, it fills it with an empty dict(except for the last argument, as that should be an zengl.Image)

        # self.cache["circle"] = {1: {(1, 2): {"31": "PRETEND THIS IS AN IMAGE"}}}

        # this was NOT fun to write.
        cache = self.cache[type_]
        gpu_img: zengl.Image  # type:ignore
        for i, arg in enumerate(args):
            if arg not in cache:  # if not initted, init
                # if last arg
                if i == len(args) - 1:
                    surf = self.func_to_type[type_](args)

                    # im not using surface.get_view() bcuz I dont want to deal with converting from bgra to rgba.
                    gpu_img = self.ctx.image(
                        surf.size,
                        format="rgba8unorm",
                    )
                    gpu_img.clear_value = (0.0, 1.0, 0.0, 1.0)
                    gpu_img.clear()
                    gpu_img.write(pygame.image.tobytes(surf, "RGBA", flipped=True))

                    cache[arg] = gpu_img
                else:  # havent arrived at last arg, continue
                    cache[arg] = {}
            cache = cache[arg]
            if i == len(args) - 1:
                gpu_img = cache

        return gpu_img
