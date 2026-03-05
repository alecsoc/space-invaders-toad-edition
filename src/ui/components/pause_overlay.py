import pygame
from typing import TYPE_CHECKING, List, Optional

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager
from src.managers.sound_player import SoundPlayer

from src.ui.components.text_label import TextLabel
from src.ui.components.option_button import OptionButton
from src.ui.components.scoreboard import Scoreboard

from src.ui.screens.options_screen import OptionsScreen

if TYPE_CHECKING:
    from src.ui.screens.in_game_screen import InGameScreen

class PauseOverlay:
    def __init__(self, game_screen: "InGameScreen") -> None:
        self.game_screen = game_screen

        self.bg_image: Optional[pygame.Surface] = AssetManager.get_image("main_bg")
        self.scoreboard: Scoreboard = Scoreboard()
        
        screen_w: int = Settings.WIDTH
        screen_h: int = Settings.HEIGHT

        center_x: int = screen_w // 2
        start_y: int = screen_h // 2 - 40
        spacing: int = 60

        self.title_label: TextLabel = TextLabel(
            x=center_x,
            y=300,
            text="JUEGO PAUSADO",
            font_key="pixel",
            font_size=80
        )
    
        self.options: List[OptionButton] = [
            OptionButton(center_x, start_y + spacing, "RESUMIR", self.on_resume, True),
            OptionButton(center_x, start_y + (spacing * 2), "OPCIONES", self.on_options),
            OptionButton(center_x, start_y + (spacing * 3), "REGRESAR AL MENÚ", self.on_quit_game),
        ]

        self.selected_index: int = 0
        self.pressed_option: Optional[OptionButton] = None
        self.transition_timer: float = 0

        self.is_active = False

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        if self.pressed_option: return

        for event in events:
            if event.type == pygame.KEYDOWN:
                previous_index: int = self.selected_index

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    SoundPlayer.play_sfx("option", 0.2)
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    SoundPlayer.play_sfx("option", 0.2)
                    self.selected_index = (self.selected_index - 1) % len(self.options)

                if previous_index != self.selected_index:
                    self.options[previous_index].set_selected(False)

                self.options[self.selected_index].set_selected(True)

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    SoundPlayer.play_sfx("select")
                    self.pressed_option = self.options[self.selected_index]
                    self.transition_timer = Settings.TRANSITION_DELAY

    def update(self, dt: float) -> None:
        self.scoreboard.update()

        if self.pressed_option:
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                self.pressed_option.action()
                self.pressed_option = None
                return
            
        return None
    
    def draw(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        self.scoreboard.draw(surface)
        self.title_label.draw(surface)
            
        for option in self.options:
            if self.pressed_option == option:
                if int(self.transition_timer * 10) % 2 == 0:
                    option.draw(surface)
            else:
                option.draw(surface)

    def on_resume(self) -> None:
        self.is_active = False
    
    def on_options(self) -> None:
        self.game_screen.game.current_screen = OptionsScreen(self.game_screen, False)

    def on_quit_game(self) -> None:
        SoundPlayer.play_music("menu_theme")
        self.game_screen.game.current_screen = self.game_screen.parent