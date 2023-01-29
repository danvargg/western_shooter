"""Game entities."""
import os
from typing import Tuple

import pygame as pg
from pygame.math import Vector2 as vector

from sprites import AllSprites


class Entity(pg.sprite.Sprite):

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
        super().__init__(groups)

        self.import_assets(path)

        self.frame_index = 0
        self.status = 'down'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200

        # collisions
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height / 2)  # FIXME: Magic numbers
        self.collision_sprites = collision_sprites

        # Attack
        self.attacking = False

    def import_assets(self, path):
        """_summary_

        Args:
            path (_type_): _description_
        """
        self.animations = {}

        for index, folder in enumerate(os.walk(path)):
            # C:\Users\devg2\edu\western_shooter\shooter\graphics\player\down_idle
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pg.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

    def move(self, dt: float):
        """_summary_

        Args:
            dt (float): _description_
        """
        # normalize
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # horiztonal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self, direction: str):
        """Collision detection.

        Args:
            direction (str): player direction
        """
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx

                else:  # vertical
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery
