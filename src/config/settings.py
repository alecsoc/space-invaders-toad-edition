from pathlib import Path
from arcade_machine_sdk import BASE_WIDTH, BASE_HEIGHT, DEFAULT_FPS

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    # Metadata
    TITLE = "Space Invaders: TOAD Edition"
    DESCRIPTION = "Implementación del clásico Space Invaders, adaptado para Taller de Objetos y Abstracción de Datos y el proyecto final 'Arcade Machine'."
    RELEASE_DATE = "1/2/2026"
    AUTHORS = ["Alejandro Capriles", "Luciano Pietrucci"]
    GROUP_NUMBER = 8

    # --- Game Parameters ---

    # --- Window Parameters ---
    WIDTH = BASE_WIDTH
    HEIGHT = BASE_HEIGHT
    FPS = DEFAULT_FPS

    # Logic Parameters (PARCIALES, SUJETOS A CAMBIOS)
    PLAYER_X = 365
    PLAYER_Y = 480
    PLAYER_SPEED = 300
    BULLET_SPEED = 500

    ENEMY_X_CHANGE = 100
    ENEMY_Y_CHANGE = 30
    ENEMY_ROWS = 3
    ENEMY_COLS = 6
    ENEMY_SPACING_X = 70
    ENEMY_SPACING_Y = 60
    ENEMY_OFFSET_X = 100
    ENEMY_OFFSET_Y = 50
    COLLISION_RADIUS = 27

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BG_COLOR = (41, 60, 94)
    YELLOW  = (0, 255, 255)

    # Assets Paths
    ASSETS_PATH = BASE_DIR / "assets"
    IMAGES_PATH = ASSETS_PATH / "images"
    SOUNDS_PATH = ASSETS_PATH / "sounds"
    FONTS_PATH = ASSETS_PATH / "fonts"

    # Assets Maps
    IMAGES_MAP = {
        "background": "galaxy-bg.png",
        "player": "space-ship.png",
        "enemy": "alien.png",
        "bullet": "bullet.png",
        "icon": "ufo.png"
    }

    SOUNDS_MAP = {
        "main_theme": "music/SITB-Theme.wav",
        "shoot": "sfx/shoot-ship.wav",
        "explosion": "sfx/hit-enemy.wav"
    }

    FONTS_MAP = {
        "pixel": "score_text.ttf"
    }

    # Dict for AssetManager
    IMAGES = {}
    SOUNDS = {}
    FONTS = {}
