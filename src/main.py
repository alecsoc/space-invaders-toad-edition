import pygame
from arcade_machine_sdk import GameMeta
from config.settings import Settings
from game import Game

def main():
    metadata = (
        GameMeta()
            .with_title(Settings.TITLE)
            .with_description(Settings.DESCRIPTION)
            .with_release_date(Settings.RELEASE_DATE)
            .with_group_number(Settings.GROUP_NUMBER)
            .add_tag("Arcade")
            .add_tag("Retro")
            .add_tag("Shooter")
            .with_authors(Settings.AUTHORS)
    )

    game = Game(metadata)

    if __name__ == "__main__":
        game.run_independently()

if __name__ == "__main__":
    main()