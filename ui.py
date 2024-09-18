import pygame
import mili

from constants import SIZE, SCREEN_RECT


class UI:
    def __init__(self) -> None:
        self.surface = pygame.Surface(SIZE, pygame.SRCALPHA)
        self.changed = False
        self.mili = mili.MILI(self.surface)

    def _init_structure(self):
        m = self.mili
        with m.begin(SCREEN_RECT, {}):
            m.rect()

    def render(self):
        if self.changed:
            self._draw()
            self.changed = False
            return self.surface
        return None

    def _draw(self): ...
