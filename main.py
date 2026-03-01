import pygame
from arcade_machine_sdk import GameMeta

from src.config.settings import Settings
from src.game import Game

metadata = (
    GameMeta()
    .with_title(Settings.TITLE)
    .with_description(Settings.DESCRIPTION)
    .with_release_date(Settings.RELEASE_DATE)
    .with_group_number(Settings.GROUP_NUMBER)
    .with_tags(Settings.TAGS)
    .with_authors(Settings.AUTHORS)
)

game = Game(metadata)

if __name__ == "__main__":
    game.run_independently()