from pathlib import Path
from arcade_machine_sdk import BASE_WIDTH, BASE_HEIGHT, DEFAULT_FPS
import pygame

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    # --- Metadata ---
    TITLE = "Space Invaders"
    DESCRIPTION = "Implementación del clásico Space Invaders, adaptado para Taller de Objetos y Abstracción de Datos y el proyecto final 'Arcade Machine'."
    RELEASE_DATE = "1/2/2026"
    TAGS = ["Arcade", "Retro", "Shooter"]
    AUTHORS = ["Alejandro Capriles", "Luciano Pietrucci", "Carlos Barranca"]
    GROUP_NUMBER = 8

    # --- Game Parameters ---

    # Window Parameters
    WIDTH = BASE_WIDTH
    HEIGHT = BASE_HEIGHT
    FPS = DEFAULT_FPS

    # Logic Parameters
    PLAYER_INITIAL_Y = 680
    PLAYER_SPEED = 350
    BULLET_SPEED = 500
    PLAYER_FIRE_COOLDOWN = 400
    PLAYER_LIVES = 3

    ENEMY_SHOOT_SPEED = 250
    ENEMY_SHOOT_COOLDOWN_MAX = 2000
    ENEMY_SHOOT_COOLDOWN_MIN = 400
    ENEMY_MAX_BULLETS = 10

    ENEMY_SPEED_BASE = 40
    ENEMY_STAGE_SPEED_INCREMENT = 10
    ENEMY_SPEED_INCREMENT = 3
    ENEMY_DROP_DISTANCE = 1
    ENEMY_MARGIN = 20
    ENEMY_X_CHANGE = 100
    ENEMY_Y_CHANGE = 5
    ENEMY_ROWS = 5
    ENEMY_COLS = 11
    ENEMY_SPACING_X = 70
    ENEMY_SPACING_Y = 55
    ENEMY_OFFSET_X = 80
    ENEMY_OFFSET_Y = 100
    COLLISION_RADIUS = 27

    SHIELD_SHAPE = [
        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1],
        [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1]
    ]
    
    TRANSITION_DELAY = 1.0

    # Colors
    class Colors:
        Background = (41, 60, 94)
        White = (255, 255, 255)
        Black = (0, 0, 0)
        Active = (255, 255, 0)
        Pressed = (200, 200, 0)

    # Assets Paths
    ASSETS_PATH = BASE_DIR / "assets"
    IMAGES_PATH = ASSETS_PATH / "images"
    SOUNDS_PATH = ASSETS_PATH / "sounds"
    FONTS_PATH = ASSETS_PATH / "fonts"

    # Assets Maps
    IMAGES_MAP = {
        "menu_bg": "menu_background.png",
        "game_bg": "gameplay_background.png",
        "player": "spaceship.png",
        "bullet": "bullet.png",
        "enemy_squid": "squid.png",
        "enemy_crab": "crab.png",
        "enemy_octopus": "octopus.png",
        "enemy_bullet": "enemy_laser.png",
        "icon": "ufo.png"
    }

    SOUNDS_MAP = {
        "main_theme": "music/galaxy_move.wav",
        "shoot": "sfx/shoot_ship.wav",
        "explosion": "sfx/hit_enemy.wav",
        "get_hurt": "sfx/hit_player.wav",
        "select": "sfx/select.wav",
        "game_over": "sfx/game_over.wav"
    }

    FONTS_MAP = {"pixel": "score_text.ttf"}

    # Dict for AssetManager
    IMAGES: dict[str, pygame.Surface] = {}
    SOUNDS: dict[str, pygame.mixer.Sound] = {}
    FONTS : dict[str, str]= {}