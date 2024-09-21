from pathlib import Path
import struct  # noqa
from typing import Literal
import sys
import platform

import pygame
import zengl  # noqa
import asyncio

# TODO: dont import if web

from constants import SIZE, PG_SUPPORTED_IMG_FORMATS
from ogl_manager import OpenGLManager
from ui import UI

WEB = sys.platform in ("emscripten", "wasi")

if not WEB:
    import zengl_extras

    zengl_extras.init()


class App:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE, pygame.OPENGL | pygame.DOUBLEBUF)
        self.ogl_manager = OpenGLManager()
        self.ui = UI(self.ogl_manager.ctx)

        self.input_img = pygame.Surface((100, 100), pygame.SRCALPHA)

        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.frame_count = 0
        self.since_start = 0.0

        self.last_point = None
        self.mode: Literal["pixel-wobble", "jello", "small", "weird"] = "pixel-wobble"

    def input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise SystemExit
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    self.mode = "jello"
                if e.key == pygame.K_2:
                    self.mode = "pixel-wobble"
                if e.key == pygame.K_3:
                    self.mode = "small"
                if e.key == pygame.K_4:
                    self.mode = "weird"
            if e.type == pygame.DROPFILE:
                filepath = Path(e.file)
                if filepath.is_file:
                    if filepath.suffix.lower() in PG_SUPPORTED_IMG_FORMATS:
                        print("imported file")
                        self.input_img = pygame.image.load(filepath.absolute())
                    else:
                        print("Unsupported Format!")
                        # TODO: display to the user that its not supported

    def update(self):
        """self.frame_count += 1
        self.since_start += self.dt
        self.ogl_manager.update_values(self.since_start)

        if not self.last_point:
            self.last_point = pygame.mouse.get_pos()

        pressed = pygame.mouse.get_pressed()
        if pressed and (pressed[0] or pressed[2] or pressed[1]):
            draw_on: pygame.Surface
            if pressed[0]:
                draw_on = self.drawable
                color = "black"
                radius = PAINT_SIZE
            elif pressed[1]:
                draw_on = self.color_surf
                color = "blue"
                radius = PAINT_SIZE
            elif pressed[2]:
                draw_on = self.drawable
                color = "white"
                radius = CLEAR_SIZE

            start = pygame.Vector2(*self.last_point)
            end = pygame.Vector2(*pygame.mouse.get_pos())

            pygame.draw.circle(draw_on, color, start, radius)

            new = start.copy()
            while True:
                new = new.move_towards(end, 2.0)
                pygame.draw.circle(draw_on, color, new, radius)
                dif = end - new
                if dif.length() < 1:
                    break
            pygame.draw.circle(draw_on, color, end, radius)
            self.last_point = end
        else:
            self.last_point = None"""

    def draw(self):
        # pygame
        self.screen.fill("white")

        self.ui.render()
        self.ui.img.blit(self.ogl_manager.mask_img)

        # drawable = black or white surf
        # self.ogl_manager.mask_img

        # zengl
        self.ogl_manager.new_frame()
        g = self.ogl_manager.ctx.image(
            self.input_img.size,
            "rgba8unorm",
            pygame.image.tobytes(self.input_img, "RGBA", flipped=True),
        )
        g.blit(self.ogl_manager.mask_img)
        self.ogl_manager.end_frame()

    async def run(self):
        while True:
            self.input()
            self.update()
            self.draw()

            self.dt = max(self.clock.tick(60) / 1000, 0.00001)
            self.fps = 1 / self.dt
            # print(self.fps)

            pygame.display.flip()
            await asyncio.sleep(0)


if __name__ == "__main__":
    app = App()
    asyncio.run(app.run())
