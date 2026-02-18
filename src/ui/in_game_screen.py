import pygame
class InGameScreen:
    def __init__(self, font_path, font_size, text_color2, keep_playing_text = " RESUME (Press Z)", stop_playing_text = "QUIT (Press X)", resume_game = True, quit_game = False):
        self.keep_playing_text = keep_playing_text
        self.stop_playing_text = stop_playing_text
        self.text_color2 = text_color2
        self.resume_game = resume_game
        self.quit_game = quit_game
        self.font_resume = pygame.font.Font(font_path, font_size // 2)

    @staticmethod
    def draw(self, surface):
              resume_surface = self.font_main.render(self.keep_playing_text, True, self.text_color2)
              resume_rect = resume_surface.get_rect(midtop=(surface.get_width() // 2, surface.get_height() // 2 - resume_surface.get_height()))

              quit_surface = self.font_main.render(self.stop_playing_text, True, self.text_color2)
              quit_rect = quit_surface.get_rect(midtop=(resume_rect.centerx, resume_rect.bottom + 15))

              surface.blit(resume_surface, resume_rect)
              surface.blit(quit_surface, quit_rect)
              pygame.display.flip()

    def handle_pause(self, key_pressed):
           
           if key_pressed == pygame.K_c:
              for event in pygame.event.get():
                 if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                       return self.resume_game

                 if event.type == pygame.K_x:
                     return self.quit_game
              
           return None
    
