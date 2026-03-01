import pygame

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.y = float(self.rect.y)
        self.speed = Settings.ENEMY_SHOOT_SPEED

    def update(self, dt):
        self.y += self.speed * dt
        self.rect.y = int(self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, points, enemy_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = float(x)
        self.y = float(y)
        self.image = image
        self.points = points
        self.enemy_type = enemy_type
        self.is_alive = True

    @staticmethod
    def create_enemy(enemy_type_key, x, y):
        try:
            img = AssetManager.get_image(enemy_type_key)
        except:
            print(f"Error cargando {enemy_type_key}")
            img = pygame.Surface((40,40))
            img.fill((255,0,0))

        if "squid" in enemy_type_key: pts = 30
        elif "crab" in enemy_type_key: pts = 20
        else: pts = 10
        
        return Enemy(x, y, img, pts, enemy_type_key)

    def update(self, dx, dy):
        if self.is_alive:
            self.x += dx
            self.y += dy

    def draw(self, surface):
        if self.is_alive:
            surface.blit(self.image, self.rect)