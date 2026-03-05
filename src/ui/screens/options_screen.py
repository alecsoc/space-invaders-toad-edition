import pygame
from typing import TYPE_CHECKING, List, Optional

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager
from src.managers.sound_player import SoundPlayer

from src.ui.base_screen import BaseScreen

from src.ui.components.text_label import TextLabel
from src.ui.components.option_button import OptionButton
from src.ui.components.integer_option_button import IntegerOptionButton

if TYPE_CHECKING:
    from src.ui.screens.main_menu_screen import MainMenu
    from src.ui.screens.in_game_screen import InGameScreen

class OptionsScreen(BaseScreen):
    def __init__(self, parent: "MainMenu | InGameScreen", is_parent_main_menu: bool) -> None:
        super().__init__(parent.game)

        self.parent = parent
        self.is_parent_main_menu = is_parent_main_menu
        self.bg_image: Optional[pygame.Surface] = AssetManager.get_image("main_bg")

        screen_w: int = Settings.WIDTH
        screen_h: int = Settings.HEIGHT

        center_x: int = screen_w // 2
        start_y: int = screen_h // 2
        spacing: int = 70
        
        self.title_label: TextLabel = TextLabel(
            x=center_x,
            y=100,
            text="OPCIONES",
            font_key="pixel",
            font_size=80
        )

        self.info_labels: List[TextLabel] = []

        self.options: List[OptionButton] = [
            IntegerOptionButton(center_x, start_y, "VOLUMEN", self.on_volume_update, True, Settings.MUSIC_VOLUME_PERCENT, 10, 100, 0, True),
            IntegerOptionButton(center_x, start_y + spacing, "SFX", self.on_sfx_update, False, Settings.SFX_VOLUME_PERCENT, 10, 100, 0, True),
            OptionButton(center_x, start_y + (spacing * 2), "VOLVER", self.on_back),
        ]

        self.selected_index: int = 0
        self.pressed_option: Optional[OptionButton] = None
        self.transition_timer: float = 0

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
                if event.key == pygame.K_RIGHT or event.key == pygame.K_s:
                    current_option = self.options[self.selected_index]
                    if isinstance(current_option, IntegerOptionButton):
                        SoundPlayer.play_sfx("option", 0.2)
                        current_option.increase()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    current_option = self.options[self.selected_index]
                    if isinstance(current_option, IntegerOptionButton):
                        SoundPlayer.play_sfx("option", 0.2)
                        current_option.decrease()

                if previous_index != self.selected_index:
                    self.options[previous_index].set_selected(False)

                self.options[self.selected_index].set_selected(True)

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    current_option = self.options[self.selected_index]
                    if not isinstance(current_option, IntegerOptionButton):
                        SoundPlayer.play_sfx("select")
                        self.pressed_option = self.options[self.selected_index]
                        self.transition_timer = Settings.TRANSITION_DELAY

    def update(self, dt: float) -> None:
        if self.pressed_option:
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                self.pressed_option.action()
                self.pressed_option = None
                return
            
        return None

    def draw(self, surface: pygame.Surface) -> None:
        if self.bg_image:
            scaled_bg: pygame.Surface = pygame.transform.scale(self.bg_image, surface.get_size())
            surface.blit(scaled_bg, (0, 0))
        else:
            surface.fill(Settings.Colors.Background)

        self.title_label.draw(surface)
        for label in self.info_labels:
            label.draw(surface)

        for option in self.options:
            if self.pressed_option == option:
                if int(self.transition_timer * 10) % 2 == 0:
                    option.draw(surface)
            else:
                option.draw(surface)

    def on_volume_update(self, value: int):
        Settings.MUSIC_VOLUME_PERCENT = value
        pygame.mixer.music.set_volume(value / 100)

    def on_sfx_update(self, value: int):
        Settings.SFX_VOLUME_PERCENT = value

    def on_back(self) -> None:
        if self.is_parent_main_menu:
            SoundPlayer.play_music("menu_theme")
        self.game.current_screen = self.parent