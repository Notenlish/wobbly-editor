import pygame
import mili

from constants import SIZE, SCREEN_RECT
from ogl_manager import OpenGLManager


class UI:
    def __init__(self, manager: OpenGLManager) -> None:
        self.surface = pygame.Surface(SIZE, pygame.SRCALPHA)
        self.bg_col = "white"

        self.changed = True

        self.manager = manager
        self.img = manager.ctx.image(SIZE, "rgba8unorm")
        self.preview_rect: pygame.Rect | None = None

        self.mili = mili.MILI(self.surface)
        self._set_sliders()
        self._ui()
        self._draw()

    def _set_sliders(self):
        """To be called only once."""
        self.sliders: list[mili.Slider] = []
        for _ in range(3):
            slider = mili.Slider(False, True, (15, 15), True)
            slider.valuex = 0.5
            self.sliders.append(slider)

    def _ui(self):
        m = self.mili
        m.start({"padx": 0})
        with m.begin(SCREEN_RECT, {"padx": 0, "pady": 2, "clip_draw": False}) as main:  # noqa F841
            with m.begin(
                None,
                style={"fillx": True, "filly": "25", "axis": "x", "clip_draw": False},
            ) as top:  # noqa
                with m.begin(
                    None,
                    {"fillx": "45", "filly": "100", "axis": "y", "padx": 0, "pady": 0},
                ) as preset_rows_container:  # noqa
                    for r in range(2):
                        with m.begin(
                            None,
                            {
                                "fillx": "100",
                                "filly": "50",
                                "axis": "x",
                                "padx": 0,
                                "pady": 0,
                            },
                        ) as preset_row:  # noqa F841
                            for i in range(2):
                                with m.begin(
                                    None,
                                    {
                                        "fillx": "50",
                                        "filly": "100",
                                        "padx": 0,
                                        "pady": 0,
                                    },
                                ) as preset:  # noqa F841
                                    m.rect(
                                        {
                                            "color": (150,) * 3,
                                            "padx": 2,
                                            "pady": 2,
                                            "border_radius": 4,
                                            "outline": 2,
                                        }
                                    )

                with m.begin(
                    None,
                    {"fillx": "55", "filly": "100", "clip_draw": False},
                    get_data=True,
                ) as sliders_container:  # noqa F841
                    slider_h = f"{100 / len(self.sliders)}"
                    for slider in self.sliders:
                        with m.begin(
                            None,
                            {"fillx": "100", "filly": slider_h} | slider.area_style,
                            get_data=True,
                        ) as slider_container:
                            slider.update_area(slider_container)  # type:ignore
                            # m.rect({"color": (40,) * 3})
                            m.rect({"color": (200,) * 3, "outline": 2})

                            handle = m.element(slider.handle_rect, slider.handle_style)
                            if handle:  # used for indentation
                                slider.update_handle(handle)

                                m.rect({"color": "white", "border_radius": 100})

                                m.rect(
                                    {
                                        "color": (150,) * 3,
                                        "outline": 2,
                                        "border_radius": 100,
                                    }
                                )

            with m.begin(
                None,
                style={"fillx": True, "filly": "75", "axis": "x"},
                header="",
                get_data=False,
            ) as bottom:  # noqa
                with m.begin(
                    None, style={"fillx": "80", "filly": "100"}, get_data=True
                ) as preview_c:  # noqa F841
                    m.rect({"color": "blue"})
                    self.preview_rect = preview_c.absolute_rect  # type:ignore
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
            self.surface.fill(self.bg_col)
            self._ui()
            self._draw()
            self.changed = True
            self.img.write(pygame.image.tobytes(self.surface, "RGBA", flipped=True))
        self.img.blit(self.manager.sc_img)

    def _draw(self):
        self.mili.update_draw()
