"""Player module."""
import sys
from typing import Tuple, Callable

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
        create_bullet: Callable
    ) -> None:
        """Initializes player.

        Args:
            pos (tuple): player position
            groups (pg.sprite.Group): sprite groups
            path (str): path to player sprites
            collision_sprites ( pg.sprite.Group): collision sprites
            create_bullet (Callable): function to create bullet
        """

        super().__init__(pos, groups, path, collision_sprites)

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

        status_mappings = {
            'left': vector(-1, 0),
            'right': vector(1, 0),
            'up': vector(0, -1),
            'down': vector(0, 1)
        }

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

                self.bullet_direction = status_mappings.get(self.status.split('_')[0], vector(0, 0))

    def animate(self, dt: float):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot:
            # exercise: give the bullet an offset so it starts next to the player
            bullet_start_pos = self.rect.center + self.bullet_direction * 80  # TODO: Magic number
            self.create_bullet(pos=bullet_start_pos, direction=self.bullet_direction)
            self.bullet_shot = True
            self.shoot_sound.play()

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pg.mask.from_surface(self.image)

    def check_death(self):
        if self.health <= 0:
            pg.quit()
            sys.exit()

    def update(self, dt: float):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)

        self.blink()

        self.check_death()
        self.vulnerability_timer()
