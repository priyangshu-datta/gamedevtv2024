import pygame
from loguru import logger
from settings import *


class Bullet(pygame.sprite.Sprite):
    image: pygame.Surface | None = None

    def __init__(self, group, pos: pygame.Vector2, dir: float | int):
        super().__init__(group)

        if Bullet.image == None:
            Bullet.image = pygame.transform.rotozoom(
                pygame.image.load(
                    "graphics/Hero-Guy/_Weapon/Bullet.png"
                ).convert_alpha(),
                0,
                0.25,
            )

        self.image = Bullet.image
        self.pos = pos
        self.dir = dir
        self.speed = 1000
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt: float):
        assert self.rect
        self.rect.centerx += self.dir * self.speed * dt
        if self.rect.right > w_W and self.dir == 1:
            self.kill()
        if self.rect.left < 0 and self.dir == -1:
            self.kill()
