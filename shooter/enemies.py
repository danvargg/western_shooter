"""Game enemies."""
from typing import Tuple

import pygame as pg
from entities import Entity

from sprites import AllSprites


class Coffin(Entity):
    """_summary_

    Args:
        Entity (_type_): _description_
    """

    def __init__(
        self, pos: Tuple[float, float], groups: AllSprites, path: str, collision_sprites: pg.sprite.Group
    ) -> None:
        """_summary_

        Args:
            pos (Tuple[float, float]): _description_
            groups (AllSprites): _description_
            path (str): _description_
            collision_sprites (pg.sprite.Group): _description_
        """
        super().__init__(pos, groups, path, collision_sprites)

        self.direction = pg.math.Vector2(-1, 0)


class Cactus(Entity):
    """_summary_

    Args:
        Entity (_type_): _description_
    """

    def __init__(
        self, pos: Tuple[float, float], groups: AllSprites, path: str, collision_sprites: pg.sprite.Group
    ) -> None:
        """_summary_

        Args:
            pos (Tuple[float, float]): _description_
            groups (AllSprites): _description_
            path (str): _description_
            collision_sprites (pg.sprite.Group): _description_
        """
        super().__init__(pos, groups, path, collision_sprites)
