from pathlib import Path
from xml.etree.ElementTree import QName
import pygame
import zengl
import struct

from utils import load_vertex_shader, load_frag_shader
from constants import PG_SUPPORTED_IMG_FORMATS


class Preview:
    def __init__(self, area: pygame.Rect, ctx: zengl.Context) -> None:
        self.area = area
        self.ctx = ctx

        self.input_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.input_surf.fill("white")
        self.input_img = ctx.image(
            self.input_surf.size,
            "rgba8unorm",
            pygame.image.tobytes(self.input_surf, "RGBA", flipped=True),
        )

        self.img = ctx.image(area.size, "rgba8unorm")
        self.pipeline = ctx.pipeline(
            vertex_shader=load_vertex_shader("preview"),
            fragment_shader=load_frag_shader("preview"),
            resources=[
                {
                    "type": "sampler",
                    "binding": 0,
                    "image": self.input_img,
                    "min_filter": "nearest",  # nearest = pixelart
                    "mag_filter": "nearest",
                    "wrap_x": "clamp_to_edge",
                    "wrap_y": "clamp_to_edge",
                }
            ],
            topology="triangle_strip",
            vertex_count=4,
            framebuffer=[self.img],
            uniforms={
                "preview_rect": struct.pack("ffff", self.area.topleft, self.area.size)
            },
        )

    def load_image(self, path: str):
        filepath = Path(path)
        if filepath.is_file:
            suffix = filepath.suffix.lower()
            if suffix in PG_SUPPORTED_IMG_FORMATS:
                print("imported file")
                self.input_surf = pygame.image.load(filepath.absolute())
                
            else:
                print("Unsupported Format!")
                # TODO: display to the user that its not supported

    def render(self): ...
