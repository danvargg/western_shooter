"""Main game loop."""
import sys

import pygame as pg
from pytmx.util_pygame import load_pygame

from settings import WINDOW_WIDTH, WINDOW_HEIGHT, PATHS
from player import Player
from sprites import AllSprites, Sprite


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
        tmx_map = load_pygame(PATHS['map_data'])

        # Tiles
        for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
            Sprite(pos=(x * 64, y * 64), surf=surf, groups=self.all_sprites)

        # Objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite(pos=(obj.x, obj.y), surf=obj.image, groups=self.all_sprites)

        # Player
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(
                    pos=(obj.x, obj.y), groups=self.all_sprites, path=PATHS['player'], collision_sprites=None
                )

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
