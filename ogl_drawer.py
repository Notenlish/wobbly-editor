import zengl
from typing import Literal
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
        byte_per_float: int = 4,
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

        self._load_shader_src()
        self._load_images()
        self._set_texarray()
        self._set_inst_buf()

        self._setup()

    def _setup(self): ...

    def _load_shader_src(self):
        with open(f"assets/shader/{self.name}.frag", "r") as f:
            self.frag_src = f.read()
        with open(f"assets/shader/{self.name}.vert", "r") as f:
            self.vert_src = f.read()

    def _set_texarray(self): ...

    def _set_inst_buf(self):
        # 16 bytes per obj(4 floats)
        self.instance_buffer = self.ctx.buffer(size=self.obj_count * 16)
        # each instanced object is a vec4(xy = pos, z = rot, w = texture_id)

    def _load_images(self): ...


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
            ctx, img, "circle", tex_size, tex_count, obj_count, byte_per_float=4
        )

    def _setup(self):
        print("WWWWWWWWWWWWWWWWWWW")
        self.instances = np.array(
            [
                np.random.uniform(0.0, SIZE[0], self.obj_count),
                np.random.uniform(0.0, SIZE[1], self.obj_count),
                np.random.uniform(0.0, np.pi, self.obj_count),
                np.random.uniform(0, self.tex_count, self.obj_count),
            ],
            "f4",
        ).T.copy()  # why is there .T here?

        # print("Buffer sizes of instance buffer and instances np array.")
        # print(self.instance_buffer.size)
        # print(len(self.instances.tobytes()))

        self.instance_buffer.write(self.instances)

        self.pipeline = self.ctx.pipeline(
            vertex_shader=self.vert_src,
            fragment_shader=self.frag_src,
            includes={
                "screen_size": f"const vec2 screen_size = vec2({SIZE[0]},{SIZE[1]});"
            },
            layout=[{"name": "Texture", "binding": 0}],
            resources=[
                {
                    "type": "sampler",
                    "binding": 0,
                    # I hit a roadblock for 3 days bcuz I wrote self.img instead of self.texture here...
                    "image": self.texture,
                    "wrap_x": "clamp_to_edge",
                    "wrap_y": "clamp_to_edge",
                }
            ],
            blend={
                "enable": True,
                # this does some kind of blending, but idk what it is
                "src_color": "src_alpha",
                "dst_color": "one_minus_src_alpha",
            },
            framebuffer=[self.img],
            topology="triangle_strip",
            vertex_count=4,
            # what is /i ?
            vertex_buffers=zengl.bind(self.instance_buffer, "4f /i", 0),
            instance_count=self.obj_count,
        )

    def render(self):
        self.instances[:, 2] += 0.02
        self.instance_buffer.write(self.instances)
        # self.img.clear()
        self.pipeline.render()

    def _load_images(self):
        byte_arr: list[bytes] = []
        for i in range(self.tex_count):
            surf = pygame.Surface(self.tex_size, pygame.SRCALPHA)
            # surf.fill((125, 0, 125, 255))

            color = [(255 // (self.tex_count - 1)) * i] * 3
            center = (self.tex_size[0] // 2, self.tex_size[1] // 2)
            rad = self.tex_size[0] // 2

            pygame.draw.circle(
                surf,
                color,
                center,
                rad,
            )

            byte_arr.append(
                pygame.image.tobytes(
                    surf,
                    "RGBA",
                    flipped=True,
                )
            )
        self.pixels = b"".join(byte_arr)
        print("Why")
        self.texture = self.ctx.image(
            size=self.tex_size,
            format="rgba8unorm",
            data=self.pixels,
            array=self.tex_count,
        )
        self.texture.write(
            self.pixels
        )  # you need to send pixels to the gpu using this.

    def _set_texarray(self):
        # print(self.pixels)
        ...
