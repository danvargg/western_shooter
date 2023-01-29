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
        """_summary_

        Args:
            player (_type_): _description_
        """
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

    def __init__(self, pos: Tuple[float, float], surf: pg.Surface, groups: list[AllSprites]) -> None:
        """_summary_

        Args:
            pos (Tuple[float, float]): _description_
            surf (pg.Surface): _description_
            groups (list[AllSprites]): _description_
        """
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)


class Bullet(pg.sprite.Sprite):
    """_summary_
    """

    def __init__(
        self, pos: pg.math.Vector2, direction: pg.math.Vector2, surf: pg.Surface, groups: list[AllSprites]
    ) -> None:
        """_summary_

        Args:
            pos (pg.math.Vector2): _description_
            direction (pg.math.Vector2): _description_
            surf (pg.Surface): _description_
            groups (list[AllSprites]): _description_
        """

        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = direction
        self.speed = 400

    def update(self, dt: float):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
