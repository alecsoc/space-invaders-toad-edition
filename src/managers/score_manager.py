import pygame
import json
import os
from src.config.settings import Settings

class ScoreManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScoreManager, cls).__new__(cls)
            cls._instance._init_manager()
        return cls._instance

    def _init_manager(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(base_path, "..", "..", "save_data.json")
        self.current_score = 0
        self.high_score = self._load_high_score()
        
    def _load_high_score(self):
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except Exception as e:
            print(f"Error al cargar puntaje: {e}")
        return 0

    def save_high_score(self):
        if self.current_score >= self.high_score:
            self.high_score = self.current_score
            try:
                with open(self.save_path, "w") as f:
                    json.dump({"high_score": self.high_score}, f)
            except Exception as e:
                print(f"Error al guardar puntaje: {e}")

    def add_points(self, points):
        self.current_score += points
        if self.current_score > self.high_score:
            self.high_score = self.current_score

    def reset_current(self):
        self.current_score = 0