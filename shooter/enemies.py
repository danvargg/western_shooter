"""Game enemies."""
from typing import Tuple

import pygame as pg
from pygame.math import Vector2 as vector

from entities import Entity
from sprites import AllSprites


class Enemy:  # TODO: no init?
    # TODO: any class attributes?

    def get_player_distance_direction(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = vector()

        return distance, direction

    def face_player(self):
        """_summary_
        """
        distance, direction = self.get_player_distance_direction()

        if distance < self.notice_radius:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0:  # player to the left
                    self.status = 'left_idle'
                elif direction.x > 0:  # player to the right
                    self.status = 'right_idle'
            else:
                if direction.y < 0:  # player to the top
                    self.status = 'up_idle'
                elif direction.y > 0:  # player to the bottom
                    self.status = 'down_idle'

    def walk_to_player(self):
        """_summary_
        """
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance < self.walk_radius:
            self.direction = direction
            self.status = self.status.split('_')[0]
        else:
            self.direction = vector()


class Coffin(Entity, Enemy):
    """_summary_

    Args:
        Entity (_type_): _description_
    """

    def __init__(
        self, pos: Tuple[float, float], groups: AllSprites, path: str, collision_sprites: pg.sprite.Group, player
    ) -> Tuple[vector, vector]:
        """_summary_

        Args:
            pos (Tuple[float, float]): _description_
            groups (AllSprites): _description_
            path (str): _description_
            collision_sprites (pg.sprite.Group): _description_
        """
        super().__init__(pos, groups, path, collision_sprites)

        # Overwrites
        self.speed = 100

        # Player interaction
        self.player = player
        self.notice_radius = 550
        self.walk_radius = 400
        self.attack_radius = 50

    def animate(self, dt: float):
        """_summary_

        Args:
            dt (float): _description_
        """
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt: float):
        """_summary_

        Args:
            dt (float): _description_
        """
        self.face_player()
        self.walk_to_player()
        self.move(dt)
        self.animate(dt)


class Cactus(Entity, Enemy):
    """_summary_

    Args:
        Entity (_type_): _description_
    """

    def __init__(
        self, pos: Tuple[float, float], groups: AllSprites, path: str, collision_sprites: pg.sprite.Group, player
    ) -> None:
        """_summary_

        Args:
            pos (Tuple[float, float]): _description_
            groups (AllSprites): _description_
            path (str): _description_
            collision_sprites (pg.sprite.Group): _description_
        """
        super().__init__(pos, groups, path, collision_sprites)

        # Overwrites
        self.speed = 100

        # Player interaction
        self.player = player
        self.notice_radius = 600
        self.walk_radius = 500
        self.attack_radius = 350

    def animate(self, dt: float):
        """_summary_

        Args:
            dt (float): _description_
        """
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt: float):
        """_summary_

        Args:
            dt (float): _description_
        """
        self.face_player()
        self.walk_to_player()
        self.move(dt)
