import pygame

from src.config.settings import Settings

class Shield(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, size: int) -> None:
        super().__init__()
        self.image: pygame.Surface = pygame.Surface((size, size))
        self.image.fill(Settings.Colors.Active)
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))