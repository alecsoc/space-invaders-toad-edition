import pygame
from config.settings import Settings

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, x_change, y_change, image):
        super().__init__()
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.image = image
        self.is_alive = True

    def get_rect(self):
        return pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height()
        )

    def update(self, dt):
        if self.is_alive:
            self.x += self.x_change * dt * 60

            if self.x <= 0 or self.x >= Settings.WIDTH - self.image.get_width():
                self.x_change *= -1
                self.y += self.y_change

    def draw(self, surface):
        if self.is_alive:
            surface.blit(self.image, (self.x, self.y))