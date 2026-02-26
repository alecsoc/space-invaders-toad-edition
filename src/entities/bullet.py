import pygame

from src.config.settings import Settings

from src.managers.sound_player import SoundPlayer

class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.pos_y = 0.0
        self.speed = speed
        self.is_active = False

    def get_rect(self):
        return self.rect

    def fire(self, player_rect):
        if not self.is_active:
            SoundPlayer.play_sfx("shoot", 0.4)
            self.rect.centerx = player_rect.centerx
            self.rect.bottom = player_rect.top
            
            self.pos_y = float(self.rect.y)
            self.is_active = True

    def update(self, dt):
        if self.is_active:
            self.pos_y -= self.speed * dt
            self.rect.y = int(self.pos_y)

            if self.rect.bottom < 0:
                self.is_active = False

    def draw(self, surface):
        if self.is_active:
            surface.blit(self.image, self.rect)