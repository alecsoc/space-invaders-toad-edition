import pygame

from src.managers.sound_player import SoundPlayer


class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed: float, image: pygame.Surface) -> None:
        super().__init__()
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.pos_y: float = 0.0
        self.speed: float = speed
        self.is_active: bool = False

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def fire(self, player_rect: pygame.Rect) -> None:
        if not self.is_active:
            SoundPlayer.play_sfx("shoot", 0.4)
            self.rect.centerx = player_rect.centerx
            self.rect.bottom = player_rect.top

            self.pos_y = float(self.rect.y)
            self.is_active = True

    def update(self, dt: float) -> None:
        if self.is_active:
            self.pos_y -= self.speed * dt
            self.rect.y = int(self.pos_y)

            if self.rect.bottom < 0:
                self.is_active = False

    def draw(self, surface: pygame.Surface) -> None:
        if self.is_active:
            surface.blit(self.image, self.rect)