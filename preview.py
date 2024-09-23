from pathlib import Path
import pygame
import zengl
from ogl_manager import OpenGLManager
import struct

from utils import load_vertex_shader, load_frag_shader
from constants import (
    PG_SUPPORTED_IMG_FORMATS,
    SC_BOTTOMLEFT,
    SC_BOTTOMRIGHT,
    SC_TOPLEFT,
    SC_TOPRIGHT,
)


class Preview:
    def __init__(self, rect: pygame.Rect | None, ogl_manager: OpenGLManager) -> None:
        self.rect = None
        self.ogl_manager = ogl_manager
        self.ctx = ogl_manager.ctx

        self.input_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.input_surf.fill("white")
        self.input_img = self.ctx.image(
            self.input_surf.size,
            "rgba8unorm",
            pygame.image.tobytes(self.input_surf, "RGBA", flipped=True),
        )

        rect = rect if rect is not None else pygame.Rect(0, 0, 1, 1)

        self._setup_pipeline(rect)

    def _setup_pipeline(self, rect: pygame.Rect):
        if self.rect != rect:
            print(rect.size)
            self.rect = rect
            self.img = self.ctx.image(rect.size, "rgba8unorm")
            self.pipeline = self.ctx.pipeline(
                vertex_shader=load_vertex_shader("preview"),
                fragment_shader=load_frag_shader("preview"),
                layout=[{"name": "Texture", "binding": 0}],
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
                uniforms={"preview_rect": (self.rect.topleft, *self.rect.size)},
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

    def render(self):
        if self.rect:
            self.pipeline.render()

            offset = SC_BOTTOMLEFT - pygame.math.Vector2(self.rect.bottomleft)
            self.img.blit(
                self.ogl_manager.sc_img, offset=(round(-offset.x), round(offset.y))
            )

    def update(self, rect: pygame.Rect | None):
        if rect:
            self._setup_pipeline(rect)
