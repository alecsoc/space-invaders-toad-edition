import pygame

from src.config.settings import Settings

from src.entities.shield import Shield

class ShieldManager:
    def __init__(self):
        self.shields = []
        self.block_size = 5
        self._create_multiple_shields()

    def _create_shield(self, start_x, start_y):
        group = pygame.sprite.Group()

        for row_index, i in enumerate(Settings.SHIELD_SHAPE):
            for col_index, j in enumerate(i):
                if j == 1:
                    x = start_x + col_index * self.block_size
                    y = start_y + row_index * self.block_size
                    
                    group.add(Shield(x, y, self.block_size))

        return group

    def _create_multiple_shields(self):
        amount = 4
        shield_width = len(Settings.SHIELD_SHAPE[0]) * self.block_size
        offset = (Settings.WIDTH - (amount * shield_width)) // (amount + 1)
        
        for i in range(amount):
            x = (i + 1) * offset + (i * shield_width)
            self.shields.append(self._create_shield(x, 520))

    def draw(self, surface):
        for obstacle in self.shields:
            obstacle.draw(surface)