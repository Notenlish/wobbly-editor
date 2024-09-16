import zengl
from typing import Literal, TypedDict, Callable
import pygame
import numpy as np

from constants import SIZE

type DrawColor = str | tuple[int, int, int] | pygame.Color
type DrawRadius = float | int
type DrawOutlineWidth = int

type DrawOptions = Literal["circle"]


class OpenGLDrawer:
    def __init__(
        self,
        ctx: zengl.Context,
        img: zengl.Image,
        name: str,
        tex_size: tuple[int, int],
        tex_count: int,
        obj_count: int = 16,
        byte_per_float: int = 2,
    ) -> None:
        self.ctx = ctx
        self.img = img  # img to render to
        self.name = name
        self.tex_size = tex_size
        self.tex_count = tex_count
        self.obj_count = obj_count
        self.byte_per_float = byte_per_float

        print(
            f"name: {name} tex_size:{tex_size}  tex_count:{tex_count}  obj_count:{obj_count}  byte_per_float:{byte_per_float}"
        )

        self.__load_shader_src()
        self.__load_images()
        self.__set_texarray()
        self.__set_inst_buf()

    def __load_shader_src(self):
        with open(f"assets/shader/{self.name}.frag", "r") as f:
            self.frag_src = f.read()
        with open(f"assets/shader/{self.name}.vert", "r") as f:
            self.vert_src = f.read()

    def __set_texarray(self): ...

    def __set_inst_buf(self):
        self.instance_buffer = self.ctx.buffer(
            size=self.obj_count * 4 * self.byte_per_float
        )
        print(self.obj_count * 4 * self.byte_per_float)
        # each instanced object is a vec4(xy = pos, z = rot, w = texture_id)

    def __load_images(self): ...


class OpenGLCircleDrawer(OpenGLDrawer):
    def __init__(
        self,
        ctx: zengl.Context,
        img: zengl.Image,
        tex_size: tuple[int, int],
        tex_count: int = 2,
        obj_count: int = 16,
    ) -> None:
        super().__init__(
            ctx, img, "circle", tex_size, tex_count, obj_count, byte_per_float=2
        )

        self.instances = np.array(
            [
                np.random.uniform(0.0, SIZE[0], obj_count),
                np.random.uniform(0.0, SIZE[1], obj_count),
                np.random.uniform(0.0, np.pi, obj_count),
                np.random.uniform(0, tex_count, obj_count),
            ],
            "f4",
        ).T.copy()  # why is there .T here?

        print(self.instance_buffer.size)
        print(self.instances.size)

        self.instance_buffer.write(self.instances)

        self.pipeline = self.ctx.pipeline(
            vertex_shader=self.vert_src,
            fragment_shader=self.frag_src,
            includes={
                "screen_size": f"const vec2 screen_size = vec2({SIZE[0]},{SIZE[1]});"
            },
        )

    def __load_images(self):
        self.pixels = []
        for i in range(self.tex_count):
            surf = pygame.Surface(self.tex_size, pygame.SRCALPHA)

            color = [(255 // (self.tex_count - 1)) * i] * 3
            center = (self.tex_size[0] // 2, self.tex_size[1] // 2)
            rad = self.tex_size[0] // 2

            pygame.draw.circle(
                surf,
                color,
                center,
                rad,
            )

            self.pixels.append(
                self.ctx.image(
                    self.tex_size,
                    "rgba8unorm",
                    pygame.image.tobytes(
                        surf,
                        "RGBA",
                        flipped=True,
                    ),
                )
            )

    def __set_texarray(self):
        self.texture = self.ctx.image(
            self.tex_size, "rgba8unorm", self.pixels, array=self.tex_count
        )
