import pygame

class Scoreboard:
    def __init__(self):
        pass

    def add_points(self, points):
        self.score += points

    def reset(self):
        self.score = 0

    def draw(self, surface):
        pass