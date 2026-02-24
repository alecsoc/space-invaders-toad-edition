import pygame


class InGameScreen:
    def __init__(
        self,
        font_path,
        font_size,
        text_color2,
        keep_playing_text="RESUME (Press Z)",
        stop_playing_text="QUIT (Press X)",
        resume_game=True,
        quit_game=False,
    ):
        self.keep_playing_text = keep_playing_text
        self.stop_playing_text = stop_playing_text
        self.text_color2 = text_color2
        self.resume_game = resume_game
        self.quit_game = quit_game

        # Cargamos la fuente (asegurándote de que font_path no sea None)
        if font_path:
            self.font_main = pygame.font.Font(font_path, font_size // 2)
        else:
            self.font_main = pygame.font.SysFont("Arial", font_size // 2)

    def draw(self, surface):
        # Creamos una capa semitransparente para el fondo de pausa
        overlay = pygame.Surface(
            (surface.get_width(), surface.get_height()), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 150))  # Negro con transparencia
        surface.blit(overlay, (0, 0))

        # Render de textos
        resume_surface = self.font_main.render(
            self.keep_playing_text, True, self.text_color2
        )
        resume_rect = resume_surface.get_rect(
            center=(surface.get_width() // 2, surface.get_height() // 2 - 20)
        )

        quit_surface = self.font_main.render(
            self.stop_playing_text, True, self.text_color2
        )
        quit_rect = quit_surface.get_rect(
            center=(surface.get_width() // 2, surface.get_height() // 2 + 40)
        )

        surface.blit(resume_surface, resume_rect)
        surface.blit(quit_surface, quit_rect)
        # Nota: No hagas display.flip() aquí, deja que el render principal lo haga

    def handle_input(self, event):
        """
        Recibe UN evento desde el loop principal de game.py
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                return "RESUME"
            if event.key == pygame.K_x:
                return "QUIT"
        return None
