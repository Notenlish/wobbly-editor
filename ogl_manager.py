import zengl
from constants import SIZE
import struct


class OpenGLManager:
    def __init__(self):
        with open("assets/shader/default.vert", "r") as f:
            vert_src = f.read()
        with open("assets/shader/default.frag", "r") as f:
            frag_src = f.read()

        self.ctx = zengl.context()

        self.mask_img = self.ctx.image(SIZE, format="rgba8unorm")
        self.mask_img.clear_value = (0, 255, 0, 255)
        self.mask_img.clear()

        self.pipeline = self.ctx.pipeline(
            vertex_shader=vert_src,
            fragment_shader=frag_src,
            framebuffer=None,  # =[self.mask_img],
            topology="triangle_strip",
            vertex_count=4,
            layout=[
                {"name": "mask_texture", "binding": 0},
                # {"name": "color_texture", "binding": 1},
            ],
            resources=[
                {
                    "type": "sampler",
                    "binding": 0,
                    "image": self.mask_img,
                    "min_filter": "nearest",
                    "mag_filter": "nearest",
                    "wrap_x": "clamp_to_edge",
                    "wrap_y": "clamp_to_edge",
                },
                # {
                #    "type": "sampler",
                #    "binding": 1,
                #    "image": self.zgl_color_img,
                #    "min_filter": "nearest",
                #    "mag_filter": "nearest",
                #    "wrap_x": "clamp_to_edge",
                #    "wrap_y": "clamp_to_edge",
                # },
            ],
            viewport=(0, 0, *SIZE),
            uniforms={
                "time": 0.0,
                # prob should use vec4 bcuz weird drivers but ill fix only if theres a problem with this
                "screen_size": SIZE,
                "effect_size": 1.0,
                "move_mul": 3.0,
                "some_mul": 50.0,
            },
        )

        self.since_start = 0

    def new_frame(self):
        self.ctx.new_frame(clear=False)

    def end_frame(self):
        self.pipeline.render()
        self.ctx.end_frame()
        self.mask_img.clear()

    def update_values(self, since_start: float):
        self.since_start = since_start
        pixel_mul = 1
        speed = 5
        self.pipeline.uniforms["time"][:] = struct.pack(  # type:ignore
            "f", (self.since_start * speed // pixel_mul) * pixel_mul
        )

    def change_state(self, new_state: str):
        # self.pipeline.uniforms["screen_size"][:] = struct.pack("ff", *SIZE)
        match new_state:
            case "pixel-wobble":
                pixel_mul = 1
                speed = 5

                # whyy
                self.pipeline.uniforms["time"][:] = struct.pack(  # type:ignore
                    "f", (self.since_start * speed // pixel_mul) * pixel_mul
                )
                self.pipeline.uniforms["effect_size"][:] = struct.pack("f", 1.0)  # type:ignore
                self.pipeline.uniforms["move_mul"][:] = struct.pack("f", 2.0)  # type:ignore
                self.pipeline.uniforms["some_mul"][:] = struct.pack("f", 2.0)  # type:ignore
            case "jello":
                self.pipeline.uniforms["time"][:] = struct.pack("f", self.since_start)  # type:ignore
                self.pipeline.uniforms["effect_size"][:] = struct.pack("f", 1.2)  # type:ignore
                self.pipeline.uniforms["move_mul"][:] = struct.pack("f", 4.5)  # type:ignore
                self.pipeline.uniforms["some_mul"][:] = struct.pack("f", 2.0)  # type:ignore
            case "small":
                # hm, I think I should both apply the small movement and the movement of "pixel-wobble"
                # either I will have to use an single shader with a bunch of uniforms(if I want customisability)
                # or just allow certain presets with each their own configured preset
                pixel_mul = 1
                speed = 8
                self.pipeline.uniforms["time"][:] = struct.pack(  # type:ignore
                    "f", (self.since_start * speed // pixel_mul) * pixel_mul
                )
                self.pipeline.uniforms["effect_size"][:] = struct.pack("f", 1.2)  # type:ignore
                self.pipeline.uniforms["move_mul"][:] = struct.pack("f", 1.2)  # type:ignore
                self.pipeline.uniforms["some_mul"][:] = struct.pack("f", 20.0)  # type:ignore
            case "weird":
                self.pipeline.uniforms["effect_size"][:] = struct.pack("f", 5.0)  # type:ignore
                self.pipeline.uniforms["time"][:] = struct.pack("f", self.since_start)  # type:ignore
                self.pipeline.uniforms["move_mul"][:] = struct.pack("f", 4.0)  # type:ignore
                self.pipeline.uniforms["some_mul"][:] = struct.pack("f", 2.2)  # type:ignore
