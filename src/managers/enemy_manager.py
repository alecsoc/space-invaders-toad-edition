import random
from typing import Optional
import pygame

from src.config.settings import Settings
from src.managers.asset_manager import AssetManager
from src.entities.enemy import Enemy, EnemyBullet


class EnemyManager:
    SPEED_SCALE: float = 8.0

    def __init__(self, stage: int = 1) -> None:
        self.stage: int = stage
        self.direction: int = 1

        self.speed: float = Settings.ENEMY_SPEED_BASE + ((stage - 1) * Settings.ENEMY_STAGE_SPEED_INCREMENT)

        self.shoot_delay: int = max(
            Settings.ENEMY_SHOOT_COOLDOWN_MIN,
            Settings.ENEMY_SHOOT_COOLDOWN_MAX - (stage * 100)
        )

        self.enemies: list[Enemy] = []
        self.bullets: list[EnemyBullet] = []
        self.last_shot: int = pygame.time.get_ticks()
        self.total_enemies: int = 0

        self._generate_group()

    def _generate_group(self) -> None:
        layout: list[str] = ["squid", "crab", "crab", "octopus", "octopus"]

        for i, type_name in enumerate(layout):
            for j in range(Settings.ENEMY_COLS):
                x: int = Settings.ENEMY_OFFSET_X + (j * Settings.ENEMY_SPACING_X)
                y: int = Settings.ENEMY_OFFSET_Y + (i * Settings.ENEMY_SPACING_Y)

                full_type_name: str = f"enemy_{type_name}"
                new_enemy: Enemy = Enemy.create_enemy(full_type_name, x, y)

                if new_enemy:
                    self.enemies.append(new_enemy)

        self.total_enemies = len(self.enemies)

    def _get_current_speed(self, alive_count: int) -> float:
        if self.total_enemies == 0:
            return self.speed

        t: float = 1.0 - ((alive_count - 1) / self.total_enemies)
        multiplier: float = 1.0 + (self.SPEED_SCALE - 1.0) * t

        return self.speed * multiplier

    def update(self, dt: float) -> Optional[str]:
        alive_enemies: list[Enemy] = [e for e in self.enemies if e.is_alive]

        if not alive_enemies:
            return "CLEARED"

        self._update_movement(alive_enemies, dt)
        self._manage_shooting(alive_enemies)
        self._update_bullets(dt)

        return None

    def _update_movement(self, alive_enemies: list[Enemy], dt: float) -> None:
        current_speed: float = self._get_current_speed(len(alive_enemies))
        dx: float = self.direction * current_speed * dt

        for alive_enemy in self.enemies:
            if alive_enemy.is_alive:
                alive_enemy.x += dx
                alive_enemy.rect.x = int(alive_enemy.x)
                alive_enemy.rect.y = int(alive_enemy.y)

        hit_edge: bool = False
        for alive_enemy in alive_enemies:
            if self.direction == 1:
                if alive_enemy.x + alive_enemy.image.get_width() >= Settings.WIDTH - 20:
                    hit_edge = True
                    break
            else:
                if alive_enemy.x <= 20:
                    hit_edge = True
                    break

        if hit_edge:
            self.direction *= -1

            for alive_enemy in self.enemies:
                if alive_enemy.is_alive:
                    alive_enemy.y += Settings.ENEMY_Y_CHANGE
                    alive_enemy.x += self.direction * 5

    def _manage_shooting(self, alive_enemies: list[Enemy]) -> None:
        now: int = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay and alive_enemies:
            if len(self.bullets) < Settings.ENEMY_MAX_BULLETS:
                shooter: Enemy = random.choice(alive_enemies)

                bullet_x: float = shooter.x + (shooter.image.get_width() // 2)
                bullet_y: float = shooter.y + shooter.image.get_height()

                new_bullet: EnemyBullet = EnemyBullet(
                    int(bullet_x),
                    int(bullet_y),
                    AssetManager.get_image("enemy_bullet")
                )
                self.bullets.append(new_bullet)
                self.last_shot = now

    def _update_bullets(self, dt: float) -> None:
        for b in self.bullets[:]:
            b.update(dt)

            if b.y > Settings.HEIGHT:
                self.bullets.remove(b)

    def draw(self, surface: pygame.Surface) -> None:
        for enemy in self.enemies:
            if enemy.is_alive:
                enemy.draw(surface)

        for bullet in self.bullets:
            bullet.draw(surface)