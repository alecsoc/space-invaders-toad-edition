from typing import Callable

from pygame import Surface

from src.ui.components.text_label import TextLabel
from src.ui.components.option_pointer import OptionPointer
from src.config.settings import Settings

class OptionButton(TextLabel):
    def __init__(self, x: int, y: int, text: str, action: Callable[[], None], initially_selected: bool = False):
        super().__init__(x, y, text, font_key="pixel")
        self.action = action
        self.__selected = False
        self.selection_pointer = OptionPointer(font_key="pixel", color=Settings.Colors.Active)
        self.set_selected(initially_selected)

    def set_selected(self, selected: bool):
        self.__selected = selected
        if self.__selected:
            self.set_color(Settings.Colors.Active)
        else:
            self.set_initial_color()
    
    def draw(self, surface: Surface) -> None:
        if self.__selected:
            x = self.x - (self.text_surface.get_width() if self.text_surface else 0) // 2 - 50
            y = self.y - 23
            self.selection_pointer.draw(surface, x, y)
        return super().draw(surface)