import pygame
from src.config.settings import Settings
from src.managers.sound_player import SoundPlayer
from arcade_machine_sdk import BASE_WIDTH


class Player(pygame.sprite.Sprite):
    ACCELERATION = 1800.0
    FRICTION = 1800.0

    def __init__(self, speed: float, image: pygame.Surface) -> None:
        super().__init__()
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.pos_x: float = 0
        self.vel_x: float = 0.0
        self.speed: float = speed

        self.lives: int = Settings.PLAYER_LIVES
        self.is_alive: bool = True
        self.is_visible: bool = True

        self.moving_left: bool = False
        self.moving_right: bool = False

        self.is_invincible: bool = False
        self.invincibility_timer: float = 0

    def set_initial_pos(self) -> None:
        self.rect.x = (BASE_WIDTH - self.image.get_width()) // 2
        self.rect.y = Settings.PLAYER_INITIAL_Y
        self.pos_x = float(self.rect.x)
        self.vel_x = 0.0           # reset velocity on repositioning

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def take_damage(self) -> str:
        SoundPlayer.play_sfx("get_hurt", 0.4)

        if self.is_invincible:
            return "INVINCIBLE"

        self.lives -= 1

        if self.lives <= 0:
            self.is_alive = False
            return "GAME_OVER"

        self.is_invincible = True
        self.invincibility_timer = 3.0
        self.set_initial_pos()

        return "LIFE_LOST"

    def get_player_input(self, e: pygame.event.Event) -> None:
        if not self.is_alive: return

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                self.moving_left = True
            if e.key == pygame.K_RIGHT:
                self.moving_right = True
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                self.moving_left = False
            if e.key == pygame.K_RIGHT:
                self.moving_right = False

    def update(self, dt: float) -> None:
        if not self.is_alive: return

        if self.is_invincible:
            self.invincibility_timer -= dt
            if self.invincibility_timer <= 0:
                self.is_invincible = False

        if self.moving_left and not self.moving_right:
            self.vel_x -= self.ACCELERATION * dt
        elif self.moving_right and not self.moving_left:
            self.vel_x += self.ACCELERATION * dt
        else:
            if self.vel_x > 0:
                self.vel_x = max(0.0, self.vel_x - self.FRICTION * dt)
            elif self.vel_x < 0:
                self.vel_x = min(0.0, self.vel_x + self.FRICTION * dt)

        self.vel_x = max(-self.speed, min(self.speed, self.vel_x))

        self.pos_x += self.vel_x * dt

        margin = 10
        if self.pos_x < margin:
            self.pos_x = float(margin)
            self.vel_x = 0.0
        elif self.pos_x > Settings.WIDTH - self.rect.width - margin:
            self.pos_x = float(Settings.WIDTH - self.rect.width - margin)
            self.vel_x = 0.0

        self.rect.x = int(self.pos_x)

    def draw(self, surface: pygame.Surface) -> None:
        if self.is_visible and self.image:
            if self.is_invincible:
                if int(self.invincibility_timer * 10) % 2 == 0:
                    surface.blit(self.image, self.rect)
            else:
                surface.blit(self.image, self.rect)