from abc import ABC, abstractmethod
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game import Game

class BaseScreen(ABC):
    def __init__(self, game: "Game"):
        self.game = game

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass