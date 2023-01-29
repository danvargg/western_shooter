"""Main game loop."""
import sys

import pygame as pg

from settings import WINDOW_WIDTH, WINDOW_HEIGHT, PATHS
from player import Player
from sprites import AllSprites


class WesternShooter:
    """_summary_
    """

    def __init__(self):
        """_summary_
        """
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Western shooter')
        self.clock = pg.time.Clock()

        # Groups
        self.all_sprites = AllSprites()

        self.setup()

    def setup(self):
        """_summary_
        """
        self.player = Player(pos=(200, 200), groups=self.all_sprites, path=PATHS['player'], collision_sprites=None)

    def run(self):
        """_summary_
        """
        while True:
            # event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            # Update groups
            self.all_sprites.update(dt=dt)

            # Draw groups
            self.display_surface.fill('black')
            self.all_sprites.customize_draw(player=self.player)

            pg.display.update()


if __name__ == '__main__':
    game = WesternShooter()
    game.run()
