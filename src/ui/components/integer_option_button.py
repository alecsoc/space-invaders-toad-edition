from src.ui.components.option_button import OptionButton
from typing import Callable

class IntegerOptionButton(OptionButton):
    def __init__(
        self, x: int,
        y: int,
        text: str,
        action: Callable[[int], None],
        initially_selected: bool = False,
        initial_value: int = 0,
        step: int = 1,
        max_value: int = 10,
        min_value: int = 0,
        is_percent: bool = False
    ):
        self.__current_value = initial_value
        self.is_percent = is_percent
        super().__init__(x, y, text, lambda: None, initially_selected)
        self.step = step
        self.max_value = max_value
        self.min_value = min_value
        self._render_surface()
        self.integer_action = action

    def increase(self):
        old_value = self.__current_value
        self.__current_value += self.step
        if self.__current_value > self.max_value:
            self.__current_value = self.max_value
        if self.__current_value != old_value:
            self.integer_action(self.__current_value)
            self._render_surface()

    def decrease(self):
        old_value = self.__current_value
        self.__current_value -= self.step
        if self.__current_value < self.min_value:
            self.__current_value = self.min_value
        if self.__current_value != old_value:
            self.integer_action(self.__current_value)
            self._render_surface()

    def get_renderable_text(self):
        return f"{self.text}: {self.__current_value}{"%" if self.is_percent else ""}"