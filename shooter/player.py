"""Player module."""
import sys
from typing import Tuple

import pygame as pg
from pygame.math import Vector2 as vector

from sprites import AllSprites
from entities import Entity


class Player(Entity):
    """Player class."""

    def __init__(
        self,
        pos: Tuple[float, float],
        groups: AllSprites,
        path: str,
        collision_sprites: pg.sprite.Group,
        create_bullet  # TODO: <class 'method'>
    ) -> None:
        """_summary_

        Args:
            pos (tuple): _description_
            groups (pg.sprite.Group): _description_
            path (str): _description_
            collision_sprites (_type_): _description_
        """

        super().__init__(pos, groups, path, collision_sprites)

        # Bullet
        self.create_bullet = create_bullet
        self.bullet_shot = False

    def get_status(self):
        """_summary_
        """
        # Idle
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # Attacking
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def input(self):
        """_summary_
        """
        keys = pg.key.get_pressed()

        if not self.attacking:

            if keys[pg.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pg.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if keys[pg.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pg.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pg.K_SPACE]:
                self.attacking = True
                self.direction = vector()
                self.frame_index = 0
                self.bullet_shot = False

                match self.status.split('_')[0]:
                    case 'left': self.bullet_direction = vector(-1, 0)
                    case 'right': self.bullet_direction = vector(1, 0)
                    case 'up': self.bullet_direction = vector(0, -1)
                    case 'down': self.bullet_direction = vector(0, 1)

    def animate(self, dt: float):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:
            # exercise: give the bullet an offset so it starts next to the player
            bullet_start_pos = self.rect.center + self.bullet_direction * 80  # TODO: Magic number
            self.create_bullet(pos=bullet_start_pos, direction=self.bullet_direction)
            self.bullet_shot = True

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]

    def check_death(self):
        if self.health <= 0:
            pg.quit()
            sys.exit()

    def update(self, dt: float):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)

        self.check_death()
        self.vulnerability_timer()
