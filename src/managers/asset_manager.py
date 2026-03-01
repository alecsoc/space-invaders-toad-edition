import pygame

from src.config.settings import Settings

class AssetManager:
    @staticmethod
    def load_all_assets():
        for name, file in Settings.IMAGES_MAP.items():
            if file is not None:
                path = Settings.IMAGES_PATH / file
                if path.exists():
                    Settings.IMAGES[name] = pygame.image.load(str(path)).convert_alpha()
                else:
                    print(f"Archivo no encontrado: {path}")
            else:
                print(f"El valor para '{name}' en IMAGES_MAP es None")

        for name, file in Settings.SOUNDS_MAP.items():
            if file is not None:
                path = Settings.SOUNDS_PATH / file
                if path.exists():
                    Settings.SOUNDS[name] = pygame.mixer.Sound(str(path))
                else:
                    print(f"Archivo no encontrado: {path}")
            else:
                print(f"El valor para '{name}' en SOUNDS_MAP es None")

        for name, file in Settings.FONTS_MAP.items():
            if file is not None:
                path = Settings.FONTS_PATH / file
                if path.exists():
                    Settings.FONTS[name] = str(path)
                else:
                    print(f"Archivo no encontrado: {path}")
            else:
                print(f"El valor para '{name}' en SOUNDS_MAP es None")

    @staticmethod
    def get_image(key):
        return Settings.IMAGES.get(key)

    @staticmethod
    def get_font(key):
        return Settings.FONTS.get(key)