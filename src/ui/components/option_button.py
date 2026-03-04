from typing import Callable

from src.ui.components.text_label import TextLabel

class OptionButton(TextLabel):
    def __init__(self, x: int, y: int, text: str, action: Callable[[], None]):
        super().__init__(x, y, text, font_key="pixel")
        self.action = action