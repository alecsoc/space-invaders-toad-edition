import pygame

from src.config.settings import Settings
from src.managers.asset_manager import AssetManager


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface) -> None:
        super().__init__()
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.y: float = float(self.rect.y)
        self.speed: float = Settings.ENEMY_SHOOT_SPEED

    def update(self, dt: float) -> None:
        self.y += self.speed * dt
        self.rect.y = int(self.y)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: pygame.Surface, points: int, enemy_type: str) -> None:
        super().__init__()
        self.image: pygame.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x: float = float(x)
        self.y: float = float(y)
        self.points: int = points
        self.enemy_type: str = enemy_type
        self.is_alive: bool = True
        self.is_visible: bool = False

    @staticmethod
    def create_enemy(enemy_type_key: str, x: int, y: int) -> "Enemy":
        img: pygame.Surface = AssetManager.get_image(enemy_type_key)

        if "squid" in enemy_type_key: pts = 30
        elif "crab" in enemy_type_key: pts = 20
        else: pts = 10

        return Enemy(x, y, img, pts, enemy_type_key)

    def update(self, dx: float, dy: float) -> None:
        if self.is_alive:
            self.x += dx
            self.y += dy

    def draw(self, surface: pygame.Surface) -> None:
        if self.is_alive and self.is_visible:
            surface.blit(self.image, self.rect)