import pygame
from typing import TYPE_CHECKING, List, Optional

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager
from src.managers.sound_player import SoundPlayer

from src.ui.base_screen import BaseScreen

from src.ui.components.text_label import TextLabel
from src.ui.components.option_button import OptionButton

if TYPE_CHECKING:
    from src.game import Game

class InstructionsScreen(BaseScreen):
    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.bg_image: Optional[pygame.Surface] = AssetManager.get_image("main_bg")

        screen_w: int = Settings.WIDTH
        screen_h: int = Settings.HEIGHT

        center_x: int = screen_w // 2
        start_y: int = 220
        line_spacing: int = 50
        
        self.title_label: TextLabel = TextLabel(
            x=center_x,
            y=100,
            text="INSTRUCCIONES",
            font_key="pixel",
            font_size=80
        )

        instructions_text: List[str] = [
            "MOVER LA NAVE: TECLAS <- -> (FLECHAS: IZQ. Y DER.)",
            "MOVER ENTRE LAS OPCIONES: ^ V (FLECHAS: ARRIBA Y ABAJO)",
            "DISPARAR CON LA NAVE: TECLA ESPACIO",
            "SELECCIONAR UNA OPCION: TECLA ENTER/ESPACIO",
            "",
            "EVITA QUE DESTRUYAN TUS BARRERAS,",
            "LIMPIA LA OLEADA DE ENEMIGOS Y",
            "PASA A LA SIGUIENTE INVASION"
        ]

        self.info_labels: List[TextLabel] = []

        for i, text in enumerate(instructions_text):
            if text == "": continue

            label: TextLabel = TextLabel(
                x=center_x,
                y=start_y + (i * line_spacing),
                text=text,
                font_key="pixel",
                font_size=28
            )

            self.info_labels.append(label)

        self.back_button: OptionButton = OptionButton(center_x, screen_h - 100, "VOLVER", self.on_back)
        self.back_button.set_color(Settings.Colors.Active)
        self.pressed_option: Optional[OptionButton] = None
        self.transition_timer: float = 0

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        if self.pressed_option: return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    SoundPlayer.play_sfx("select")
                    self.pressed_option = self.back_button
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

        if self.pressed_option == self.back_button:
            if int(self.transition_timer * 10) % 2 == 0:
                self.back_button.draw(surface)
        else:
            self.back_button.draw(surface)

    def on_back(self) -> None:
        from src.ui.screens.main_menu_screen import MainMenu
        self.game.current_screen = MainMenu(self.game)