import pygame

from src.config.settings import Settings

from src.managers.sound_player import SoundPlayer

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos_x = float(self.rect.x)
        self.speed = speed

        self.lives = Settings.PLAYER_LIVES
        self.is_alive = True
        self.is_visible = True

        self.moving_left = False
        self.moving_right = False

        self.is_invincible = False
        self.invincibility_timer = 0

    def get_rect(self):
        return self.rect
    
    def take_damage(self):
        SoundPlayer.play_sfx("get_hurt", 0.4)

        if self.is_invincible:
            return "INVINCIBLE"

        self.lives -= 1

        if self.lives <= 0:
            self.is_alive = False
            return "GAME_OVER"
        
        self.is_invincible = True
        self.invincibility_timer = 3.0
        self.pos_x = float(Settings.PLAYER_X)
        self.rect.x = int(self.pos_x)

        return "LIFE_LOST"

    def get_player_input(self, e):
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

    def update(self, dt):
        if not self.is_alive: return

        if self.is_invincible:
            self.invincibility_timer -= dt
            
            if self.invincibility_timer <= 0:
                self.is_invincible = False

        move_step = self.speed * dt

        if self.moving_left and not self.moving_right:
            self.pos_x -= move_step
        elif self.moving_right and not self.moving_left:
            self.pos_x += move_step

        margin = 10

        if self.pos_x < margin:
            self.pos_x = margin
        elif self.pos_x > Settings.WIDTH - self.rect.width - margin:
            self.pos_x = Settings.WIDTH - self.rect.width - margin

        self.rect.x = int(self.pos_x)

    def draw(self, surface):
        if self.is_visible and self.image:
            if self.is_invincible:
                if int(self.invincibility_timer * 10) % 2 == 0:
                    surface.blit(self.image, self.rect)
            else:
                surface.blit(self.image, self.rect)