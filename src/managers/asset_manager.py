import pygame
from src.config.settings import Settings


class AssetManager:
    @staticmethod
    def load_all_assets() -> None:
        for name, file in Settings.IMAGES_MAP.items():
            path = Settings.IMAGES_PATH / file
            if path.exists():
                Settings.IMAGES[name] = pygame.image.load(str(path)).convert_alpha()
            else:
                print(f"Archivo no encontrado: {path}")

        for name, file in Settings.SOUNDS_MAP.items():
            path = Settings.SOUNDS_PATH / file
            if path.exists():
                Settings.SOUNDS[name] = pygame.mixer.Sound(str(path))
            else:
                print(f"Archivo no encontrado: {path}")

        for name, file in Settings.FONTS_MAP.items():
            path = Settings.FONTS_PATH / file
            if path.exists():
                Settings.FONTS[name] = str(path)
            else:
                print(f"Archivo no encontrado: {path}")

    @staticmethod
    def get_image(key: str) -> pygame.Surface:
        image = Settings.IMAGES.get(key)
        if not image:
            raise NameError("Imagen no encontrada")
        return image

    @staticmethod
    def get_font(key: str) -> str:
        font = Settings.FONTS.get(key)
        if not font:
            raise NameError("Fuente no encontrada")
        return font