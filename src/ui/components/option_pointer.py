import pygame
from src.managers.asset_manager import AssetManager
from typing import Optional, Tuple
from src.config.settings import Settings


class OptionPointer:
    def __init__(
        self,
        font_key: Optional[str] = None,
        font_size: int = 50,
        color: Tuple[int, int, int] = Settings.Colors.White
    ) -> None:
        self.font_key = font_key
        self.font_size = font_size
        self.font = AssetManager.get_font_instance_or_default(self.font_key, self.font_size)
        self.color = color
        self.text_surface = self.font.render(">", True, self.color)

    def draw(self, surface: pygame.Surface, x: int, y: int):
        surface.blit(self.text_surface, (x, y))