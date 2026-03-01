from typing import TypedDict

import pygame

from src.config.settings import Settings
from src.managers.score_manager import ScoreManager
from src.ui.components.text_label import TextLabel


class LabelConfig(TypedDict):
    x: int
    y: int
    text: str
    size: int


class Scoreboard:
    def __init__(self) -> None:
        self.manager: ScoreManager = ScoreManager()

        screen_w: int = Settings.WIDTH

        fin_x: int = screen_w - 100
        init_x: int = 100
        margin_top: int = 50
        gap: int = margin_top * 2

        text_size: int = 30

        config: list[LabelConfig] = [
            {"x": init_x, "y": margin_top, "text": "SCORE", "size": text_size},
            {"x": init_x, "y": gap, "text": "0000", "size": text_size},
            {"x": fin_x, "y": margin_top, "text": "HI-SCORE", "size": text_size},
            {"x": fin_x, "y": gap, "text": "0000", "size": text_size},
        ]

        self.labels: list[TextLabel] = [
            TextLabel(
                x=c["x"],
                y=c["y"],
                text=c["text"],
                font_key="pixel",
                font_size=c["size"]
            ) for c in config
        ]

    def update(self) -> None:
        self.labels[1].set_text(str(self.manager.current_score).zfill(4))
        self.labels[3].set_text(str(self.manager.high_score).zfill(4))

    def draw(self, surface: pygame.Surface) -> None:
        for label in self.labels:
            label.draw(surface)