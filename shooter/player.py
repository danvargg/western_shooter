"""Player module."""
import os

import pygame as pg
from pygame.math import Vector2 as vector


class Player(pg.sprite.Sprite):
    """Player class."""

    def __init__(self, pos: tuple, groups: pg.sprite.Group, path: str, collision_sprites) -> None:
        """Initializes the player

        Args:
            pos (tuple): Player position
            groups (_type_): _description_
            path (str): Player assets path
            collision_sprites (_type_): _description_
        """
        super().__init__(groups)

        self.import_assets(path)

        self.frame_index = 0
        self.status = 'down_idle'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200

        # collisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites

    def import_assets(self, path):
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

    def input(self):
        keys = pg.key.get_pressed()

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

    def move(self, dt: float):
        # normalize
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # horiztonal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        # horizontal collision

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt: float):
        self.input()
        self.move(dt)
        self.animate(dt)