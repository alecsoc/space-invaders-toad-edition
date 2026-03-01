import pygame

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager

class TextLabel:
    def __init__(
        self,
        x,
        y,
        text="",
        color=Settings.COLORS["white"],
        font_key=None,
        font_size=50,
        alpha=None,
        border=None,
    ):
        self.x, self.y = x, y
        self.text = text
        self.font_key = font_key
        self.font_size = font_size
        self.alpha = alpha
        self.border = border  # (Color, Thickness, Padding, Radius)

        self.colors = {
            "normal": color, 
            "active": color, 
            "pressed": color
        }
        self.state = "normal"

        self.font = self._load_custom_font(self.font_key, self.font_size)
        self.image = None
        self.rect = pygame.Rect(x, y, 0, 0)
        self._render_surface()

    def _load_custom_font(self, key, size):
        try:
            font_path = AssetManager.get_font(key)
            if font_path:
                return pygame.font.Font(font_path, size)
        except Exception as e:
            print(f"Error al cargar la fuente {key}: {e}")

        return pygame.font.SysFont("sans-serif", size)

    def config_option(self, active_color, pressed_color):
        self.colors["active"] = active_color
        self.colors["pressed"] = pressed_color

        self._render_surface()
        return self

    def set_state(self, state):
        if state in self.colors and self.state != state:
            self.state = state
            self._render_surface()

    def _render_surface(self):
        current_color = self.colors[self.state]
        self.image = self.font.render(self.text, True, current_color)

        if self.alpha is not None:
            self.image.set_alpha(self.alpha)

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        if self.border:
            border_color, thickness, padding, radius = self.border
            border_rect = self.rect.inflate(padding * 2, padding * 2)

            pygame.draw.rect(
                surface,
                border_color,
                border_rect,
                width=thickness,
                border_radius=radius,
            )

        surface.blit(self.image, self.rect)

    def update_text(self, new_text):
        if self.text != new_text:
            self.text = new_text
            self._render_surface()

    def update_color(self, new_color, state="normal"):
        if self.colors[state] != new_color:
            self.colors[state] = new_color

            if self.state == state:
                self._render_surface()