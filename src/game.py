import pygame
from arcade_machine_sdk import GameBase, GameMeta

from src.managers.asset_manager import AssetManager
from src.managers.sound_player import SoundPlayer

from src.ui.screens.main_menu_screen import MainMenu
from src.ui.base_screen import BaseScreen

class Game(GameBase):
    def __init__(self, metadata: GameMeta) -> None:
        super().__init__(metadata)

    def start(self, surface: pygame.Surface) -> None:
        super().start(surface)

        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        if not pygame.font.get_init():
            pygame.font.init()

        AssetManager.load_all_assets()
        self.current_screen: BaseScreen = MainMenu(self)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        self.current_screen.handle_events(events)
        
    def update(self, dt: float) -> None:
        if not self._running:
            return
        
        if self.current_screen:
            self.current_screen.update(dt)

    def render(self) -> None:
        self.surface.fill((0, 0, 0)) 
    
        if self.current_screen:
            self.current_screen.draw(self.surface)
        
        pygame.display.flip()

    def stop(self) -> None:
        SoundPlayer.stop_all()
        super().stop()