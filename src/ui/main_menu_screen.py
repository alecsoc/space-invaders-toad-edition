import pygame

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager
from src.managers.sound_player import SoundPlayer

from src.ui.components.text_label import TextLabel
from src.ui.components.scoreboard import Scoreboard
from src.ui.base_screen import BaseScreen
from typing import Callable
from src.managers.score_manager import ScoreManager
from typing import TYPE_CHECKING
from src.ui.in_game_screen import InGameScreen

if TYPE_CHECKING:
    from src.game import Game

class MenuOptionButton(TextLabel):
    def __init__(self, x: int, y: int, text: str, action: Callable[[], None]):
        super().__init__(x, y, text, font_key="pixel")
        self.action = action
    

class MainMenu(BaseScreen):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self.bg_image = AssetManager.get_image("main_bg")

        self.scoreboard = Scoreboard()

        screen_w = Settings.WIDTH
        screen_h = Settings.HEIGHT

        center_x = screen_w // 2
        start_y = screen_h // 2
        spacing = 90

        self.title_group = [
            TextLabel(
                x=center_x, 
                y=int(((screen_h // 4.5) + (i * 80))),
                text=text.upper(), 
                font_key="pixel", 
                font_size=100 if i < 2 else 45
            )
            for i, text in enumerate(["SPACE", "INVADERS"])
        ]

        self.options = [
            MenuOptionButton(center_x, start_y, "JUGAR", self.on_play),
            MenuOptionButton(center_x, start_y + spacing, "INSTRUCCIONES", self.on_instructions),
            MenuOptionButton(center_x, start_y + (spacing * 2), "CRÉDITOS", self.on_credits),
            MenuOptionButton(center_x, start_y + (spacing * 3), "SALIR", self.on_exit),
        ]

        self.selected_index = 0
        self.options[self.selected_index].set_color(Settings.Colors.Active)
        self.pressed_option = None
        self.transition_timer = 0

    def handle_events(self, events: list[pygame.event.Event]):
        if self.pressed_option:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                previous_index = self.selected_index
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_index = (self.selected_index - 1) % len(self.options)

                if previous_index != self.selected_index:
                    self.options[previous_index].set_initial_color()

                self.options[self.selected_index].set_color(Settings.Colors.Active)

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    SoundPlayer.play_sfx("select")
                    self.pressed_option = self.options[self.selected_index]
                    self.transition_timer = Settings.TRANSITION_DELAY
    
    def update(self, dt: float):
        self.scoreboard.update()

        if self.pressed_option:
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                self.pressed_option.action()
                self.pressed_option = None
                return
            
        return None
    
    def draw(self, surface: pygame.Surface):
        if self.bg_image:
            scaled_bg = pygame.transform.scale(self.bg_image, surface.get_size())
            surface.blit(scaled_bg, (0, 0))
        else:
            surface.fill(Settings.Colors.Background)

        self.scoreboard.draw(surface)

        for label in self.title_group:
            label.draw(surface)

        for option in self.options:
            if self.pressed_option == option:
                if int(self.transition_timer * 10) % 2 == 0:
                    option.draw(surface)
            else:
                option.draw(surface)

    def on_play(self):
        ScoreManager().reset_current()
        self.game.current_screen = InGameScreen(self.game)

    def on_instructions(self):
        print("Iniciando instrucciones...")

    def on_credits(self):
        print("Iniciando créditos...")

    def on_exit(self):
        self.game.stop()