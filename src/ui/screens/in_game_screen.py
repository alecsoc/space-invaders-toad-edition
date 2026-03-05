import pygame
from typing import TYPE_CHECKING, List, Optional

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager
from src.managers.sound_player import SoundPlayer
from src.managers.score_manager import ScoreManager
from src.managers.enemy_manager import EnemyManager
from src.managers.shield_manager import ShieldManager

from src.ui.base_screen import BaseScreen

from src.ui.components.text_label import TextLabel
from src.ui.components.scoreboard import Scoreboard
from src.ui.components.game_over import GameOverComponent

from src.entities.bullet import Bullet
from src.entities.player import Player

if TYPE_CHECKING:
    from src.ui.screens.main_menu_screen import MainMenu

class InGameScreen(BaseScreen):
    def __init__(self, parent: "MainMenu") -> None:
        super().__init__(parent.game)

        self.parent = parent
        self.bg_image: Optional[pygame.Surface] = AssetManager.get_image("main_bg")
        self.scoreboard: Scoreboard = Scoreboard()
        self.shield_manager: ShieldManager = ShieldManager()
        
        self.current_stage: int = 1
        self.margin_top: int = 50
        self.center_x: int = Settings.WIDTH // 2
        self.stage_label = TextLabel(self.center_x, self.margin_top, "STAGE " + str(self.current_stage), font_key="pixel")

        self.game_over: bool = False
        self.game_over_hud: GameOverComponent = GameOverComponent()
        self.return_to_menu_timer: float = 5.0

        self.bullets: List[Bullet] = []
        self.last_player_shot: int = 0

        self.pending_action: Optional[str] = None
        self.transition_timer: float = 0
        self._setup_entities()

    def _setup_entities(self) -> None:
        self.game_over = False
        self.return_to_menu_timer = 5.0
        self.bullets = []

        SoundPlayer.play_music("main_theme")
        
        self.player: Player = Player(
            speed=Settings.PLAYER_SPEED,
            image=AssetManager.get_image("player")
        )
        self.player.set_initial_pos()

        self.enemy_manager: EnemyManager = EnemyManager(stage=self.current_stage)

    def _handle_defeat(self) -> None:
        self.game_over = True
        SoundPlayer.stop_music()
        SoundPlayer.play_sfx("game_over", 1.0)
        ScoreManager().save_high_score()

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        if self.game_over:
            return
        
        for e in events:
            self.player.get_player_input(e)

            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                now = pygame.time.get_ticks()

                if now - self.last_player_shot > Settings.PLAYER_FIRE_COOLDOWN:
                    self._fire_bullet()
                    self.last_player_shot = now

        return
    
    def _fire_bullet(self) -> None:
        new_bullet: Bullet = Bullet(
            speed=Settings.BULLET_SPEED,
            image=AssetManager.get_image("bullet")
        )

        new_bullet.fire(self.player.get_rect())
        self.bullets.append(new_bullet)
    
    def update(self, dt: float) -> None:
        if self.game_over:
            self.return_to_menu_timer -= dt

            if self.return_to_menu_timer <= 0:
                SoundPlayer.play_music("menu_theme")
                self.game.current_screen = self.parent
                return
        
            return None

        self.player.update(dt)
        self.scoreboard.update()

        status = self.enemy_manager.update(dt)

        if status == "CLEARED":
            self.current_stage += 1
            self.stage_label.set_text("STAGE " + str(self.current_stage))
            self.shield_manager.generate_shields()
            self._setup_entities()

            return None
        
        for player_bullet in self.bullets[:]:
            player_bullet.update(dt)

            if not player_bullet.is_active:
                self.bullets.remove(player_bullet)
                continue

            for enemy in self.enemy_manager.enemies:
                if enemy.is_alive and player_bullet.get_rect().colliderect(enemy.rect.scale_by(0.9)):
                    enemy.is_alive = False
                    player_bullet.is_active = False
                    SoundPlayer.play_sfx("explosion", 0.2)
                    ScoreManager().add_points(enemy.points)
                    break

            if player_bullet.is_active:
                for shield_group in self.shield_manager.shields:
                    if pygame.sprite.spritecollide(player_bullet, shield_group, True):
                        player_bullet.is_active = False
                        break

        for enemy_bullet in self.enemy_manager.bullets[:]:
            hit_shield: bool = False

            for shield_group in self.shield_manager.shields:
                if pygame.sprite.spritecollide(enemy_bullet, shield_group, True):
                    self.enemy_manager.bullets.remove(enemy_bullet)
                    hit_shield = True
                    break

            if hit_shield: continue

            if enemy_bullet.rect.colliderect(self.player.get_rect().scale_by(0.8)):
                result: str = self.player.take_damage()
    
                if result != "INVINCIBLE":
                    self.enemy_manager.bullets.remove(enemy_bullet)
                    
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

    def draw(self, surface: pygame.Surface) -> None:
        if self.bg_image:
            scaled_bg: pygame.Surface = pygame.transform.scale(self.bg_image, surface.get_size())
            surface.blit(scaled_bg, (0, 0))
        else:
            surface.fill(Settings.Colors.Background)

        self.shield_manager.draw(surface)
        self.enemy_manager.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)
        self.player.draw(surface)
        self.scoreboard.draw(surface)

        self.stage_label.draw(surface)

        if self.game_over:
            self.game_over_hud.draw(surface)

        self._draw_lives_icons(surface)

    def _draw_lives_icons(self, surface):
        img = AssetManager.get_image("player")

        if img:
            life_icon = pygame.transform.scale(img, (25, 20))
            for i in range(self.player.lives):
                x = 20 + (i * 35)
                y = Settings.HEIGHT - 35
                surface.blit(life_icon, (x, y))