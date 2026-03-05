import pygame
from src.config.settings import Settings
from src.ui.components.text_label import TextLabel

class GameOverComponent:
    def __init__(self):
        screen_w = Settings.WIDTH
        screen_h = Settings.HEIGHT
        
        self.label = TextLabel(
            x=screen_w // 2,
            y=screen_h // 2,
            text="GAME OVER",
            font_key="pixel",
            font_size=80
        )

    def draw(self, surface: pygame.Surface):
        if int(pygame.time.get_ticks() / 500) % 2 == 0:
            self.label.draw(surface)