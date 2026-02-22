import pygame
from arcade_machine_sdk import GameBase

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager
from src.managers.sound_player import SoundPlayer

from src.ui.main_menu_screen import MainMenu

class Game(GameBase):
    def __init__(self, metadata) -> None:
        super().__init__(metadata)

    def start(self, surface: pygame.Surface) -> None:
        super().start(surface)

        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        if not pygame.font.get_init():
            pygame.font.init()

        AssetManager.load_all_assets()

        SoundPlayer.play_music("main_theme")

        self.screens = {
            "MAIN_MENU": MainMenu(),
        }

        self.current_screen = self.screens["MAIN_MENU"]

    def _process_screen_result(self, result: str) -> None:
        if result == "GOTO_GAMEPLAY":
            print("Creando e iniciando gameplay...")
        elif result == "GOTO_INSTR":
            print("Iniciando instrucciones...")
        elif result == "GOTO_CREDITS":
            print("Iniciando créditos...")
        elif result == "GOTO_MENU":
            self.current_screen = self.screens["MAIN_MENU"]
        elif result == "EXIT":
            self.stop()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        result = self.current_screen.handle_events(events)
        
        if result:
            self._process_screen_result(result)

    def update(self, dt: float) -> None:
        if not self._running:
            return
        
        if self.current_screen:
            result = self.current_screen.update(dt)

            if result:
                self._process_screen_result(result)

    def render(self) -> None:
        self.current_screen.draw(self.surface)

    def stop(self) -> None:
        print("Deteniendo Space Invaders...")
        SoundPlayer.stop_all()
        super().stop()