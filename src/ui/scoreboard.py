import pygame

class Scoreboard:
    def __init__(self, font_path, font_size, text_color, text_color2, i_g_scoreboard, h_scoreboard, list_of_scoreboards):
        self.i_g_scoreboard = 0
        self.h_scoreboard = h_scoreboard
        self.text_color = text_color
        self.game_font = pygame.font.Font(font_path, font_size)
        #ligeramente mas al centro
        self.pos_left = (13, 13)
        self.pos_right = (1267, 13)
        self.list_of_scoreboards = []
        self.text_color2= text_color2


    def add_points(self, points):
        self.i_g_scoreboard += points

    def reset(self):
        self.list_of_scoreboards.append(self.i_g_scoreboard)
        self.i_g_scoreboard = 0

    def highest_score(self):
        if self.list_of_scoreboards[0] == None:
            return 0
        high_score = self.list_of_scoreboards[0]
        for i in self.list_of_scoreboards:
            if i > high_score:
                self.h_scoreboard = i
        return self.h_scoreboard
            
    def draw(self, surface):
        text_surface_normalscore = self.game_font.render(f"Score : {self.i_g_scoreboard}", True, self.text_color)
        text_surface_highestscore = self.game_font.render(f"Highest Actual Score : {self.h_scoreboard}", True, self.text_color2)
        surface.bilt(text_surface_normalscore, self.pos_left)
        surface.blit(text_surface_highestscore, self.pos_right)
