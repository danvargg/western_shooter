"""Main game loop."""
import sys

import pygame as pg
from pytmx.util_pygame import load_pygame

from settings import WINDOW_WIDTH, WINDOW_HEIGHT, PATHS
from player import Player
from sprites import AllSprites, Sprite, Bullet
from enemies import Coffin, Cactus


class WesternShooter:
    """Game class."""

    def __init__(self):
        """Initialize the game."""
        pg.init()
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Western shooter')
        self.clock = pg.time.Clock()
        self.bullet_surf = pg.image.load(PATHS['bullet']).convert_alpha()

        # Groups
        self.all_sprites = AllSprites()
        self.obstacles = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        self.setup()

    def create_bullet(self, pos: pg.math.Vector2, direction: pg.math.Vector2) -> None:
        # FIXME: can't shoot in diagonal
        Bullet(pos=pos, direction=direction, surf=self.bullet_surf, groups=[self.all_sprites, self.bullets])

    def setup(self):
        """Setup map, fence, objects, and entities."""
        tmx_map = load_pygame(PATHS['map_data'])

        # Tiles
        for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
            Sprite(pos=(x * 64, y * 64), surf=surf, groups=[self.all_sprites, self.obstacles])

        # Objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite(pos=(obj.x, obj.y), surf=obj.image, groups=[self.all_sprites, self.obstacles])

        # Player
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS['player'],
                    collision_sprites=self.obstacles,
                    create_bullet=self.create_bullet,
                )

            if obj.name == 'Coffin':
                Coffin(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS['coffin'],
                    collision_sprites=self.obstacles,
                    player=self.player
                )

            if obj.name == 'Cactus':
                Cactus(
                    pos=(obj.x, obj.y),
                    groups=self.all_sprites,
                    path=PATHS['cactus'],
                    collision_sprites=self.obstacles,
                    player=self.player
                )

    def run(self):
        """Game loop."""
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
