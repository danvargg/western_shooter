"""Main game loop."""
import sys

import pygame as pg

from settings import WINDOW_WIDTH, WINDOW_HEIGHT, PATHS
from player import Player


class Game:
    def __init__(self):
        """Initialize game."""
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Western shooter')
        self.clock = pg.time.Clock()

        # Groups
        self.all_sprites = pg.sprite.Group()

        self.setup()

    def setup(self):
        Player(pos=(200, 200), groups=self.all_sprites, path=PATHS['player'], collision_sprites=None)

    def run(self):
        """Main game loop."""
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
            self.all_sprites.draw(self.display_surface)

            pg.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
