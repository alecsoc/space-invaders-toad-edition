import pygame
from src.config.settings import Settings
from src.managers.asset_manager import AssetManager
from typing import Optional, Tuple


class TextLabel:
    def __init__(
        self,
        x: int,
        y: int,
        text: str = "",
        color: Tuple[int, int, int] = Settings.Colors.White,
        font_key: Optional[str] = None,
        font_size: int = 50,
        alpha: Optional[int] = None,
        border: Optional[Tuple[Tuple[int, int, int], int, int, int]] = None,
    ) -> None:
        self.x, self.y = x, y
        self.text = text
        self.font_key = font_key
        self.font_size = font_size
        self.alpha = alpha
        self.border = border

        self.__initial_color = color
        self.color = color

        self.font = self._load_custom_font(self.font_key, self.font_size)
        self.text_surface: Optional[pygame.Surface] = None
        self.rect: pygame.Rect = pygame.Rect(x, y, 0, 0)
        self._render_surface()

    def _load_custom_font(self, key: Optional[str], size: int) -> pygame.font.Font:
        if key:
            font_path = AssetManager.get_font(key)
            if font_path:
                return pygame.font.Font(font_path, size)

        return pygame.font.SysFont("sans-serif", size)

    def draw(self, surface: pygame.Surface) -> None:
        if self.border:
            border_color, thickness, padding, radius = self.border
            border_rect = self.rect.inflate(padding * 2, padding * 2)

            pygame.draw.rect(
                surface,
                border_color,
                border_rect,
                width=thickness,
                border_radius=radius,
            )

        if self.text_surface:
            surface.blit(self.text_surface, self.rect)

    def _render_surface(self) -> None:
        self.text_surface = self.font.render(self.text, True, self.color)

        if self.alpha is not None:
            self.text_surface.set_alpha(self.alpha)

        self.rect = self.text_surface.get_rect(center=(self.x, self.y))

    def set_text(self, new_text: str) -> None:
        if self.text != new_text:
            self.text = new_text
            self._render_surface()

    def set_initial_color(self) -> None:
        self.set_color(self.__initial_color)

    def set_color(self, new_color: Tuple[int, int, int]) -> None:
        if self.color != new_color:
            self.color = new_color
            self._render_surface()