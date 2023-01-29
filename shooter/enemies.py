"""Game enemies."""
from typing import Tuple

import pygame as pg
from pygame.math import Vector2 as vector

from player import Player
from entities import Entity
from sprites import AllSprites


class Enemy:
    """Enemy base class."""

    def get_player_distance_direction(self) -> Tuple[vector, vector]:
        """_summary_

        Returns:
            Tuple[vector, vector]: _description_
        """
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = vector()

        return distance, direction

    def face_player(self) -> None:
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

    def walk_to_player(self) -> None:
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

    def __init__(self, pos: Tuple[float, float], groups: AllSprites, path: str,
                 collision_sprites: pg.sprite.Group, player: Player) -> None:
        """_summary_

        Args:
            pos (Tuple[float, float]): _description_
            groups (AllSprites): _description_
            path (str): _description_
            collision_sprites (pg.sprite.Group): _description_
            player (Player): _description_
        """
        super().__init__(pos, groups, path, collision_sprites)

        # Overwrites
        self.speed = 100

        # Player interaction
        self.player = player
        self.notice_radius = 550
        self.walk_radius = 400
        self.attack_radius = 50

    def attack(self) -> None:
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0

        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self, dt: float) -> None:
        """_summary_

        Args:
            dt (float): _description_
        """
        current_animation = self.animations[self.status]

        if int(self.frame_index) == 4 and self.attacking:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.player.damage()

        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt: float) -> None:
        """_summary_

        Args:
            dt (float): _description_
        """
        self.face_player()
        self.walk_to_player()
        self.attack()
        self.move(dt)
        self.animate(dt)

        self.check_death()
        self.vulnerability_timer()


class Cactus(Entity, Enemy):
    """_summary_

    Args:
        Entity (_type_): _description_
    """

    def __init__(self, pos: Tuple[float, float], groups: AllSprites, path: str,
                 collision_sprites: pg.sprite.Group, player: Player, create_bullet) -> None:
        """_summary_

        Args:
            pos (Tuple[float, float]): _description_
            groups (AllSprites): _description_
            path (str): _description_
            collision_sprites (pg.sprite.Group): _description_
            player (Player): _description_
        """
        super().__init__(pos, groups, path, collision_sprites)

        # Overwrites
        self.speed = 90

        # Player interaction
        self.player = player
        self.notice_radius = 600
        self.walk_radius = 500
        self.attack_radius = 350

        self.create_bullet = create_bullet
        self.bullet_shot = False

    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0
            self.bullet_shot = False

        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animate(self, dt: float) -> None:
        """_summary_

        Args:
            dt (float): delta time
        """
        current_animation = self.animations[self.status]

        if int(self.frame_index) == 6 and self.attacking and not self.bullet_shot:
            direction = self.get_player_distance_direction()[1]
            pos = self.rect.center + direction * 150
            self.create_bullet(pos, direction)
            self.bullet_shot = True

        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt: float) -> None:
        """_summary_

        Args:
            dt (float): _description_
        """
        self.face_player()
        self.walk_to_player()
        self.attack()
        self.move(dt)
        self.animate(dt)

        self.check_death()
        self.vulnerability_timer()
