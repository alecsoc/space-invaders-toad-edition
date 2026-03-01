import pygame

from src.config.settings import Settings
from src.entities.shield import Shield


class ShieldManager:
    def __init__(self) -> None:
        self.shields: list[pygame.sprite.Group] = []
        self.block_size: int = 5
        self._create_multiple_shields()

    def _create_shield(self, start_x: int, start_y: int) -> pygame.sprite.Group:
        group: pygame.sprite.Group = pygame.sprite.Group()

        for row_index, i in enumerate(Settings.SHIELD_SHAPE):
            for col_index, j in enumerate(i):
                if j == 1:
                    x: int = start_x + col_index * self.block_size
                    y: int = start_y + row_index * self.block_size

                    group.add(Shield(x, y, self.block_size))

        return group

    def _create_multiple_shields(self) -> None:
        amount: int = 4
        shield_width: int = len(Settings.SHIELD_SHAPE[0]) * self.block_size
        offset: int = (Settings.WIDTH - (amount * shield_width)) // (amount + 1)

        for i in range(amount):
            x: int = (i + 1) * offset + (i * shield_width)
            self.shields.append(self._create_shield(x, 520))

    def draw(self, surface: pygame.Surface) -> None:
        for obstacle in self.shields:
            obstacle.draw(surface)