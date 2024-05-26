import pygame
from settings import *
from random import randint, randrange, random


class Drone(pygame.sprite.Sprite):
    image: pygame.Surface = pygame.image.load(
        "graphics/Hero-Guy/_Weapon/Bullet.png"
    ).convert_alpha()

    def __init__(
        self, groups, player: pygame.sprite.Sprite, dir=pygame.Vector2(1, 0.5)
    ) -> None:
        super().__init__(groups)
        self.image = Drone.image
        self.rect = self.image.get_frect(center=(0, 0))
        self.dir = dir
        self.speed = 200
        self.player = player
        self.far = True

    def update(self, dt) -> None:
        assert self.rect
        self.rect.center += self.dir * self.speed * dt
        assert self.player.rect
        if pygame.Vector2(self.rect.center).distance_to(self.player.rect.center) < 200:
            self.speed = 400
            self.far = False
            self.dir = (
                pygame.Vector2(self.player.rect.center) - self.rect.center
            ).normalize()
        if self.far:
            self.speed = 200
            self.far = True

        if self.rect.bottom >= w_H:
            self.rect.bottom = w_H
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= w_W:
            self.rect.right = w_W
        if self.rect.bottom >= w_H or self.rect.top <= 0:
            self.dir.y *= -1
        if self.rect.left <= 0 or self.rect.right >= w_W:
            self.dir.x *= -1
