import pygame

from src.config.settings import Settings

from src.managers.asset_manager import AssetManager

from src.ui.components.text_label import TextLabel
from src.ui.components.scoreboard import Scoreboard

class MainMenu:
    def __init__(self):
        self.bg_image = AssetManager.get_image("menu_bg")

        self.scoreboard = Scoreboard()

        screen_w = Settings.WIDTH
        screen_h = Settings.HEIGHT

        center_x = screen_w // 2
        start_y = screen_h // 2
        spacing = 90

        self.title_group = [
            TextLabel(
                x=center_x, 
                y=((screen_h // 5) + (i * 80)),
                text=text.upper(), 
                font_key="pixel", 
                font_size=100 if i < 2 else 45
            )
            for i, text in enumerate(["SPACE", "INVADERS"])
        ]

        self.options = {
            "PLAY": TextLabel(
                x=center_x, 
                y=start_y, 
                text="JUGAR", 
                font_key="pixel",
            )
            .config_option(
                Settings.COLORS["active_yellow"], 
                Settings.COLORS["pressed_yellow"]
            ),
            "INSTRUCTIONS": TextLabel(
                x=center_x,
                y=start_y + spacing,
                text="INSTRUCCIONES",
                font_key="pixel"
            )
            .config_option(
                Settings.COLORS["active_yellow"], 
                Settings.COLORS["pressed_yellow"]
            ),
            "CREDITS": TextLabel(
                x=center_x,
                y=start_y + (spacing * 2),
                text="CRÉDITOS",
                font_key="pixel"
            )
            .config_option(
                Settings.COLORS["active_yellow"], 
                Settings.COLORS["pressed_yellow"]
            ),
            "QUIT": TextLabel(
                x=center_x, 
                y=start_y + (spacing * 3), 
                text="SALIR", 
                font_key="pixel"
            )
            .config_option(
                Settings.COLORS["active_yellow"], 
                Settings.COLORS["pressed_yellow"]
            ),
        }

        self.navigation_map = {
            "PLAY": {
                "up": "QUIT",
                "down": "INSTRUCTIONS",
                "next": "GOTO_GAMEPLAY"
            },
            "INSTRUCTIONS": {
                "up": "PLAY",
                "down": "CREDITS",
                "next": "GOTO_INSTR"
            },
            "CREDITS": {
                "up": "INSTRUCTIONS",
                "down": "QUIT",
                "next": "GOTO_CREDITS",
            },
            "QUIT": {
                "up": "CREDITS",
                "down": "PLAY",
                "next": "EXIT"
            }
        }

        self.current_selection = "PLAY"
        self.options[self.current_selection].set_state("active")

        self.pending_action = None
        self.transition_timer = 0

    def handle_events(self, events):
        if self.pending_action:
            return None

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.options[self.current_selection].set_state("normal")
                
                if event.key == pygame.K_DOWN:
                    self.current_selection = self.navigation_map[self.current_selection]["down"]
                elif event.key == pygame.K_UP:
                    self.current_selection = self.navigation_map[self.current_selection]["up"]

                self.options[self.current_selection].set_state("active")

                if event.key == pygame.K_RETURN:
                    action = self.navigation_map[self.current_selection]["next"]

                    if action == "EXIT":
                        return action    

                    self.options[self.current_selection].set_state("pressed")
                    self.pending_action = action
                    self.transition_timer = Settings.TRANSITION_DELAY

        return None
    
    def update(self, dt):
        self.scoreboard.update()

        if self.pending_action:
            self.transition_timer -= dt

            if self.transition_timer <= 0:
                action = self.pending_action
                self.pending_action = None
                return action
            
        return None
    
    def draw(self, surface):
        if self.bg_image:
            scaled_bg = pygame.transform.scale(self.bg_image, surface.get_size())
            surface.blit(scaled_bg, (0, 0))
        else:
            surface.fill(Settings.COLORS["bg_color"])

        self.scoreboard.draw(surface)

        for label in self.title_group:
            label.draw(surface)

        for key, option in self.options.items():
            if key == self.current_selection and self.pending_action:
                if int(self.transition_timer * 10) % 2 == 0:
                    option.draw(surface)
            else:
                option.draw(surface)