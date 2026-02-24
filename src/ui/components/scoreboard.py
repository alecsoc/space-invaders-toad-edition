from src.config.settings import Settings

from src.managers.score_manager import ScoreManager

from src.ui.components.text_label import TextLabel

class Scoreboard:
    def __init__(self):
        self.manager = ScoreManager()

        screen_w = Settings.WIDTH
        screen_h = Settings.HEIGHT

        center_x = screen_w // 2
        start_y = screen_h // 2
        spacing = 90

        text_size = 25

        config = [
            {"x": 100, "y": 30, "text": "SCORE", "size": text_size},
            {"x": 100, "y": 65, "text": "0000", "size": text_size},
            {"x": center_x, "y": 30, "text": "HI-SCORE", "size": text_size},
            {"x": center_x, "y": 65, "text": "0000", "size": text_size},
        ]

        self.labels = [
            TextLabel(
                x=c["x"],
                y=c["y"],
                text=c["text"],
                font_key="pixel",
                font_size=c["size"]
            ) for c in config
        ]

    def update(self):
        self.labels[1].update_text(str(self.manager.current_score).zfill(4))
        self.labels[3].update_text(str(self.manager.high_score).zfill(4))

    def draw(self, surface):
        for label in self.labels:
            label.draw(surface)