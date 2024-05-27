import pygame
from settings import *
from random import randint, randrange, random


class Drone(pygame.sprite.Sprite):
    image: pygame.Surface | None = None

    def __init__(
        self, groups, player: pygame.sprite.Sprite, dir=pygame.Vector2(1, 0.5)
    ) -> None:
        super().__init__(groups)

        if Drone.image == None:
            Drone.image = pygame.image.load(
                "graphics/Hero-Guy/_Weapon/Bullet.png"
            ).convert_alpha()

        self.image = Drone.image
        self.rect = self.image.get_frect(center=(0, 0))
        self.dir = dir
        self.speed = randrange(200, 300)
        self.player = player
        self.far = True

        self.change_dir_event = pygame.event.custom_type()
        self.change_dir_timer = pygame.time.set_timer(self.change_dir_event, 500)

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
        else:
            events = pygame.event.get()

            for event in events:
                if event.type == self.change_dir_event and random() > 0.5:
                    self.dir = (
                        pygame.Vector2((randint(1, w_W), randint(1, w_H)))
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
