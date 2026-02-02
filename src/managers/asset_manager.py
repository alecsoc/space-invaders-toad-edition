import pygame
from config.settings import Settings

class AssetManager:
    @staticmethod
    def load_all_assets():
        for name, file in Settings.IMAGES_MAP.items():
            path = Settings.IMAGES_PATH / file
            Settings.IMAGES[name] = pygame.image.load(str(path)).convert_alpha()

        for name, file in Settings.SOUNDS_MAP.items():
            path = Settings.SOUNDS_PATH / file
            Settings.SOUNDS[name] = pygame.mixer.Sound(str(path))

        for name, file in Settings.FONTS_MAP.items():
            path = Settings.FONTS_PATH / file
            Settings.FONTS[name] = str(path)