import random
import pygame

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager

from src.entities.enemy import Enemy, EnemyBullet

class EnemyManager:
    def __init__(self, stage=1):
        self.stage = stage
        self.direction = 1 
        
        self.speed = Settings.ENEMY_SPEED_BASE + ((stage - 1) * Settings.ENEMY_SPEED_INCREMENT)
        
        self.shoot_delay = max(
            Settings.ENEMY_SHOOT_COOLDOWN_MIN, 
            Settings.ENEMY_SHOOT_COOLDOWN_MAX - (stage * 100)
        )

        self.enemies = []
        self.bullets = []
        self.last_shot = pygame.time.get_ticks()
        
        self._generate_group()

    def _generate_group(self):
        layout = ["squid", "crab", "crab", "octopus", "octopus"]
        
        for i, type_name in enumerate(layout):
            for j in range(Settings.ENEMY_COLS):
                x = Settings.ENEMY_OFFSET_X + (j * Settings.ENEMY_SPACING_X)
                y = Settings.ENEMY_OFFSET_Y + (i * Settings.ENEMY_SPACING_Y)
                
                full_type_name = f"enemy_{type_name}"

                new_enemy = Enemy.create_enemy(full_type_name, x, y)

                if new_enemy:
                    self.enemies.append(new_enemy)

    def update(self, dt):
        alive_enemies = [e for e in self.enemies if e.is_alive]
        
        if not alive_enemies:
            return "CLEARED"

        self._update_movement(alive_enemies, dt)
        self._manage_shooting(alive_enemies)
        self._update_bullets(dt)
        
        return None

    def _update_movement(self, alive_enemies, dt):
        dx = self.direction * self.speed * dt

        for e in self.enemies:
            if e.is_alive:
                e.x += dx

                e.rect.x = int(e.x) 
                e.rect.y = int(e.y)

        hit_edge = False
        for e in alive_enemies:
            if self.direction == 1:
                if e.x + e.image.get_width() >= Settings.WIDTH - 20:
                    hit_edge = True

                    break
            else:
                if e.x <= 20:
                    hit_edge = True

                    break
        
        if hit_edge:
            self.direction *= -1

            for e in self.enemies:
                if e.is_alive:
                    e.y += Settings.ENEMY_Y_CHANGE 
                    e.x += self.direction * 5 

    def _manage_shooting(self, alive_enemies):
        now = pygame.time.get_ticks()
        
        if now - self.last_shot > self.shoot_delay and alive_enemies:
            
            if len(self.bullets) < Settings.ENEMY_MAX_BULLETS:
                shooter = random.choice(alive_enemies)
                
                bullet_x = shooter.x + (shooter.image.get_width() // 2)
                bullet_y = shooter.y + shooter.image.get_height()
                
                new_bullet = EnemyBullet(
                    bullet_x, 
                    bullet_y, 
                    AssetManager.get_image("enemy_bullet")
                )
                self.bullets.append(new_bullet)
                
                self.last_shot = now

    def _update_bullets(self, dt):
        for b in self.bullets[:]:
            b.update(dt)

            if b.y > Settings.HEIGHT:
                self.bullets.remove(b)

    def draw(self, surface):
        for b in self.bullets: b.draw(surface)

        for e in self.enemies: 
            if e.is_alive: e.draw(surface)