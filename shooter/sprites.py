"""Game sprites."""
from typing import Tuple

import pygame as pg
from pygame.math import Vector2 as vector

from settings import PATHS, WINDOW_WIDTH, WINDOW_HEIGHT


class AllSprites(pg.sprite.Group):
    """Sprite class."""

    def __init__(self) -> None:
        """_summary_
        """
        super().__init__()

        self.offset = vector()
        self.display_surface = pg.display.get_surface()
        self.bg = pg.image.load(PATHS['background']).convert()  # TODO: why only convert?

    def customize_draw(self, player):
        # Change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # Blit the surfaces
        self.display_surface.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


class Sprite(pg.sprite.Sprite):
    """_summary_

    Args:
        pg (_type_): _description_
    """

    def __init__(self, pos: Tuple[float, float], surf, groups) -> None:
        """_summary_

        Args:
            pos (Tuple[float, float]): _description_
            surf (_type_): _description_
            groups (_type_): _description_
        """
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)