import pygame

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager
from src.managers.sound_player import SoundPlayer
from src.managers.score_manager import ScoreManager
from src.managers.enemy_manager import EnemyManager
from src.managers.shield_manager import ShieldManager

from src.ui.components.scoreboard import Scoreboard
from src.ui.components.game_over import GameOverComponent

from src.entities.bullet import Bullet
from src.entities.player import Player

class InGameScreen:
    def __init__(self):
        self.bg_image = AssetManager.get_image("menu_bg")
        self.scoreboard = Scoreboard()
        self.shield_manager = ShieldManager()
        
        self.current_stage = 1
        self.game_over = False
        self.game_over_hud = GameOverComponent()
        self.return_to_menu_timer = 5.0

        self.bullets = []
        self.last_player_shot = 0

        self.pending_action = None
        self.transition_timer = 0

    def reset_game(self):
        ScoreManager().reset_current() 
        self.current_stage = 1
        self.shield_manager = ShieldManager()
        self._setup_entities()

    def _setup_entities(self):
        self.game_over = False
        self.return_to_menu_timer = 5.0
        self.bullets = []

        SoundPlayer.play_music("main_theme")
        
        self.player = Player(
            x=Settings.PLAYER_X,
            y=Settings.PLAYER_Y,
            speed=Settings.PLAYER_SPEED,
            image=AssetManager.get_image("player")
        )

        self.enemy_manager = EnemyManager(stage=self.current_stage)

    def _handle_defeat(self):
        self.game_over = True
        SoundPlayer.stop_music()
        SoundPlayer.play_sfx("game_over")
        ScoreManager().save_high_score()

    def handle_events(self, events):
        if self.game_over: return None
        
        for e in events:
            self.player.get_player_input(e)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                now = pygame.time.get_ticks()

                if now - self.last_player_shot > Settings.PLAYER_FIRE_COOLDOWN:
                    self._fire_bullet()
                    self.last_player_shot = now

        return None
    
    def _fire_bullet(self):
        new_bullet = Bullet(
            speed=Settings.BULLET_SPEED,
            image=AssetManager.get_image("bullet")
        )

        new_bullet.fire(self.player.get_rect())
        self.bullets.append(new_bullet)
    
    def update(self, dt):
        if self.game_over:
            self.return_to_menu_timer -= dt

            if self.return_to_menu_timer <= 0:
                return "GOTO_MENU"
        
            return None

        self.player.update(dt)
        self.scoreboard.update()

        status = self.enemy_manager.update(dt)

        if status == "CLEARED":
            self.current_stage += 1
            self._setup_entities()

            return None
        
        for b in self.bullets[:]:
            b.update(dt)

            if not b.is_active:
                self.bullets.remove(b)
                
                continue

            for enemy in self.enemy_manager.enemies:
                if enemy.is_alive and b.get_rect().colliderect(enemy.rect):
                    enemy.is_alive = False
                    b.is_active = False
                    SoundPlayer.play_sfx("explosion", 0.2)
                    ScoreManager().add_points(enemy.points)

                    break

            if b.is_active:
                for shield_group in self.shield_manager.shields:
                    if pygame.sprite.spritecollide(b, shield_group, True):
                        b.is_active = False

                        break

        for e_bullet in self.enemy_manager.bullets[:]:
            hit_shield = False

            for shield_group in self.shield_manager.shields:
                if pygame.sprite.spritecollide(e_bullet, shield_group, True):
                    self.enemy_manager.bullets.remove(e_bullet)
                    hit_shield = True

                    break

            if hit_shield: continue

            if e_bullet.rect.colliderect(self.player.get_rect()):
                result = self.player.take_damage()
    
                if result != "INVINCIBLE":
                    self.enemy_manager.bullets.remove(e_bullet)
                    
                if result == "GAME_OVER":
                    self._handle_defeat()
                    
                break

        for enemy in self.enemy_manager.enemies:
            if not enemy.is_alive: continue
            
            for shield_group in self.shield_manager.shields:
                pygame.sprite.spritecollide(enemy, shield_group, True)

            if enemy.rect.bottom >= self.player.rect.top:
                self._handle_defeat()

                break

        return None

    def draw(self, surface):
        if self.bg_image:
            scaled_bg = pygame.transform.scale(self.bg_image, surface.get_size())
            surface.blit(scaled_bg, (0, 0))
        else:
            surface.fill(Settings.COLORS["bg_color"])

        self.shield_manager.draw(surface)
        self.enemy_manager.draw(surface)
        for b in self.bullets: b.draw(surface)
        self.player.draw(surface)
        self.scoreboard.draw(surface)

        if self.game_over:
            self.game_over_hud.draw(surface)
        
        self._draw_lives_icons(surface)

    def _draw_lives_icons(self, surface):
        if self.player.image:
            life_icon = pygame.transform.scale(self.player.image, (25, 20))
            for i in range(self.player.lives):
                x = 20 + (i * 35)
                y = Settings.HEIGHT - 35
                surface.blit(life_icon, (x, y))