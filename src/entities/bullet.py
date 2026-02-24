import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.image = image
        self.is_active = False

    def get_rect(self):
        return pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height()
        )

    def fire(self, x, y, player_width):
        if not self.is_active:
            self.x = x + (player_width - self.image.get_width()) // 2
            self.y = y
            self.is_active = True

    def update(self, dt):
        if self.is_active:
            self.y -= self.speed * dt * 60
            if self.y <= 0:
                self.is_active = False

    def draw(self, surface):
        if self.is_active:
            surface.blit(self.image, (self.x, self.y))