import pygame
class PrincipalMenu:
    #color blanco
    def __init__(self, font_path, font_size, text_color, text_color2, start_text = "Jugar (Oprime Enter)", quit_text = "Quitar Juego (Oprime T)", text_rule = "Reglas (Oprime L)", rules_text1 = "C (Pausar Juego)", 
                 rules_text2 = "W = Arriba, S = Abajo, A = Izquierda, D = Derecha", rules_text3 = "Z (Continuar Juego)"):
       self.text_color = text_color
       self.text_color2 = self.text_color2
       self.start_text = start_text
       self.quit_text = quit_text
       self.font_start = pygame.font.Font(font_path, font_size)
       self.font_rules = pygame.font.Font(font_path, font_size // 2)
       self.rules_text1 = rules_text1
       self.rules_text2 = rules_text2
       self.rules_text3 = rules_text3
       self.text_rule = text_rule


    def draw(self, surface):

        texts = [
            self.start_text,
            self.text_rule,
            self.quit_text
        ]
        y = surface.get_height() // 2 - 50

        for text in texts:
           text_surface = self.font_rules.render(text, True, self.text_color2)
           text_rect = text_surface.get_rect(center=(surface.get_width() // 2, y))
           surface.blit(text_surface, text_rect)
           y += text_surface.get_height() + 10  

    @staticmethod
    def draw_rules(self, surface):
        rules = [
        self.rules_text1,
        self.rules_text2,
        self.rules_text3
    ]
        y = surface.get_height() // 2 - 50

        for rule in rules:
           rule_surface = self.font_rules.render(rule, True, self.text_color2)
           rule_rect = rule_surface.get_rect(center=(surface.get_width() // 2, y))
           surface.blit(rule_surface, rule_rect)
           y += rule_surface.get_height() + 10  
        pygame.display.flip()
        


        #for event in pygame.event.get():
         #   if event.type == pygame.KEYDOWN:
           #    if event.key == pygame.K_z:
            #     paused = not paused
        #if paused:
         #   InGameScreen.draw(paused)

        """start_surface = self.font_start.render(self.start_text, True, self.text_color)
        start_rect = start_surface.get_rect(midtop=(surface.get_width() // 2, surface.get_height() // 2 - start_surface.get_height()))

        rule_surface = self.font_start.render(self.text_rule, True, self.text_color2)
        rule_rect = rule_surface.get_rect(midtop=(start_rect.centerx, start_rect.bottom + 22))

        surface.blit(start_surface, start_rect)
        surface.blit(rule_surface, rule_rect)"""