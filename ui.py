import pygame
import mili

from constants import SIZE, SCREEN_RECT
from zengl import Context


class UI:
    def __init__(self, ctx: Context) -> None:
        self.surface = pygame.Surface(SIZE, pygame.SRCALPHA)
        self.changed = True
        self.mili = mili.MILI(self.surface)
        self.img = ctx.image(SIZE, "rgba8unorm")

        self._init_structure()

    def _init_structure(self):
        sliders = [mili.Slider(False, True, [20, 20]) for _ in range(3)]

        m = self.mili
        m.start()
        with m.begin(SCREEN_RECT, {}) as main:  # noqa
            with m.begin(
                None, style={"fillx": True, "filly": "40", "axis": "x"}
            ) as top:  # noqa
                with m.begin(None, {"fillx": "25", "filly": "100"}) as file_drop_area:  # noqa
                    m.rect({"color": "green", "padx": "10", "pady": "10"})

                with m.begin(
                    None, {"fillx": "25", "filly": "100", "axis": "y"}
                ) as preset_rows_container:  # noqa
                    for r in range(2):
                        with m.begin(
                            None, {"fillx": "100", "filly": "50", "axis": "x"}
                        ) as preset_row:  # noqa
                            for i in range(2):
                                with m.begin(
                                    None, {"fillx": "50", "filly": "100"}
                                ) as preset:
                                    m.rect({"padx": "10", "pady": "10", "color": "red"})

                with m.begin(
                    None, {"fillx": "50", "filly": "100"}, get_data=True
                ) as sliders_container:
                    slider_h = f"{100 / len(sliders)}"
                    for slider in sliders:
                        with m.begin(
                            None, {"fillx": "100", "filly": slider_h}
                        ) as slider_container:
                            slider.update_area(slider_container)  # type:ignore
                            # will be fixed in the next mili ui release
                            # check here: https://github.com/damusss/mili/blob/main/guide/utility.md
                            

            with m.begin(None, style={"fillx": True, "filly": "60"}) as bottom:  # noqa
                with m.begin(None, style={"fillx": "80", "filly": "100"}) as preview_c:  # noqa
                    m.rect({"color": "blue"})
                with m.begin(None, style={"fillx": "20", "filly": "100"}) as exports:  # noqa
                    with m.begin(
                        None, style={"fillx": "100", "filly": "80"}
                    ) as export_opts:  # noqa
                        m.rect({"color": "purple"})
                    with m.begin(
                        None, style={"fillx": "100", "filly": "20"}
                    ) as export_but:  # noqa
                        m.rect({"color": "gray"})

    def render(self):
        if self.changed:
            self._draw()
            self.changed = False
            self.img.write(pygame.image.tobytes(self.surface, "RGBA", flipped=True))

    def _draw(self):
        self.mili.update_draw()
