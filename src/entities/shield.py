import pygame

from src.config.settings import Settings

class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(Settings.COLORS["active_yellow"])
        self.rect = self.image.get_rect(topleft=(x, y))