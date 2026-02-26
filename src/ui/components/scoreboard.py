from src.config.settings import Settings

from src.managers.score_manager import ScoreManager

from src.ui.components.text_label import TextLabel

class Scoreboard:
    def __init__(self):
        self.manager = ScoreManager()

        screen_w = Settings.WIDTH

        fin_x = screen_w - 100
        init_x = 100
        margin_top = 50
        gap = margin_top * 2

        text_size = 30

        config = [
            {"x": init_x, "y": margin_top, "text": "SCORE", "size": text_size},
            {"x": init_x, "y": gap, "text": "0000", "size": text_size},
            {"x": fin_x, "y": margin_top, "text": "HI-SCORE", "size": text_size},
            {"x": fin_x, "y": gap, "text": "0000", "size": text_size},
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