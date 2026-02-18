import pygame
from arcade_machine_sdk import GameBase

# Configuración y Managers
from config.settings import Settings
from managers.asset_manager import AssetManager
from managers.sound_player import SoundPlayer

class Game(GameBase):
    def __init__(self, metadata):
        super().__init__(metadata)
        
        self.is_game_over = False
        
        # TO-DO #1: Se instanciarán en start()
        self.player = None
        self.enemies = []
        self.bullets = []

    def start(self, surface: pygame.Surface) -> None:
        super().start(surface)

        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Cargar todos los assets
        AssetManager.load_all_assets()
        
        # Iniciar tema principal
        SoundPlayer.play_music("main_theme")
        
        # Preparación de lógica (véase 'TO-DO #1')
        self.is_game_over = False
        print(f"--- {Settings.TITLE} Iniciado ---")

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        pausa = False
        for e in events:
            # Ejemplo de salida rápida (SUJETA A CAMBIOS)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.stop()
        for event in pygame.event.get():
            if event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pausa = True
                    confirmation = InGameScreen.pause(pausa)
            if not confirmation:
                pygame.display.flip()
                    
                    
            
            # TO-DO #2: Aquí irá la lógica de: self.player.handle_input(event)

    def update(self, dt: float) -> None:
        if not self._running or self.is_game_over:
            return

        # TO-DO #3: Ejemplo de lo que vendrá:
        # self.player.update(dt)
        pass

    def render(self) -> None:
        self.surface.fill(Settings.BG_COLOR)
        
        bg = Settings.IMAGES.get("background")
        if bg:
            self.surface.blit(bg, (0, 0))

        # TO-DO #4: El renderizado de entidades vendrá aquí:
        # if self.player: self.player.draw(self.surface)

    def stop(self) -> None:
        print("Deteniendo Space Invaders...")
        SoundPlayer.stop_all()
        super().stop()
