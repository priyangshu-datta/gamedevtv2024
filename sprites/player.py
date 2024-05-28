from enum import Enum, StrEnum, auto
from pathlib import Path

import pygame

from settings import w_H, w_W
from sprites.bullet import Bullet


class PlayerState(StrEnum):
    IDLE = auto()
    RUNNING = auto()
    JUMPING = auto()
    SHOOTING = auto()
    HURT = auto()
    DEAD = auto()


class PlayerFaceDir(Enum):
    LEFT = auto()
    RIGHT = auto()


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, collision_sprities: pygame.sprite.Group):
        super().__init__(groups)
        self.groups = groups
        self.collision_sprities = collision_sprities
        self.state = PlayerState.IDLE
        self.image_index = 0
        self.images = {
            PlayerState.IDLE: [
                Player._correct_size(pygame.image.load(path).convert_alpha())
                for path in Path("graphics/Hero-Guy/_Mode-Gun/01-Idle").glob("*.png")
            ],
            PlayerState.JUMPING: [
                Player._correct_size(pygame.image.load(path).convert_alpha())
                for path in Path("graphics/Hero-Guy/_Mode-Gun/05-Jump").glob("*.png")
            ],
            PlayerState.RUNNING: [
                Player._correct_size(pygame.image.load(path).convert_alpha())
                for path in Path("graphics/Hero-Guy/_Mode-Gun/02-Run").glob("*.png")
            ],
            PlayerState.SHOOTING: [
                Player._correct_size(pygame.image.load(path).convert_alpha())
                for path in Path("graphics/Hero-Guy/_Mode-Gun/03-Shot").glob("*.png")
            ],
            PlayerState.HURT: [
                Player._correct_size(pygame.image.load(path).convert_alpha())
                for path in Path("graphics/Hero-Guy/_Mode-Gun/04-Hurt").glob("*.png")
            ],
            PlayerState.DEAD: [
                Player._correct_size(pygame.image.load(path).convert_alpha())
                for path in Path("graphics/Hero-Guy/06-Die").glob("*.png")
            ],
        }
        self.face_dir = 1
        self.dir = pygame.Vector2(1, 0)
        self.image = self.images[self.state][self.image_index]
        self.rect = self.image.get_frect(midbottom=(w_W / 2, -800))
        self.old_rect = self.rect.copy()
        self.speed = 500
        self.gravity = 1000
        self.base = w_H - 32
        self.jumping = False
        self.jump_height = 600
        self.actions = [
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_SPACE,
            pygame.K_UP,
        ]
        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown_dur = 500

    @staticmethod
    def _correct_size(surface: pygame.Surface):
        return pygame.transform.rotozoom(surface, 0, 0.25)

    def _flip_face(self):
        assert self.image
        self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

    def shoot_timer(self):
        if self.can_shoot:
            return

        if pygame.time.get_ticks() - self.shoot_time >= self.cooldown_dur:
            self.can_shoot = True

    def shoot(self):
        assert self.rect
        self.state = PlayerState.SHOOTING
        if self.face_dir == -1:
            bullet_start_pos = pygame.Vector2(
                self.rect.midleft[0], self.rect.midleft[1]
            )
        else:
            bullet_start_pos = pygame.Vector2(
                self.rect.midright[0], self.rect.midright[1]
            )

        bullet_start_pos += (bullet_start_pos - self.rect.midtop) / 2
        Bullet(self.groups, bullet_start_pos, self.face_dir)

    def move(self, dt):
        assert self.rect

        self.rect.centerx += self.dir.x * self.speed * dt
        self.collision("horizontal")

        if self.jumping:
            self.state = PlayerState.JUMPING
            self.dir.y = -self.jump_height
            self.jumping = False

        self.dir.y += 0.5 * self.gravity * dt
        self.rect.y += self.dir.y * dt
        self.dir.y += 0.5 * self.gravity * dt
            
        self.collision("vertical")

    def action(self):
        keys = pygame.key.get_pressed()

        if not any([keys[action_key] for action_key in self.actions]):
            self.state = PlayerState.IDLE
            self.dir.x = 0
            return

        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.state = PlayerState.RUNNING
            self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            self.face_dir = self.dir.x

        if keys[pygame.K_UP]:
            self.jumping = True

        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def collision(self, axis):
        for sprite in self.collision_sprities:
            if sprite.rect.colliderect(self.rect):

                assert self.rect
                if axis == "horizontal":
                    if (
                        self.rect.left <= sprite.rect.right
                        and self.old_rect.left >= sprite.old_rect.right
                    ):
                        self.rect.left = sprite.rect.right

                    if (
                        self.rect.right >= sprite.rect.left
                        and self.old_rect.right <= sprite.old_rect.left
                    ):
                        self.rect.right = sprite.rect.left

                if axis == "vertical":

                    if (
                        self.rect.top <= sprite.rect.bottom
                        and self.old_rect.top >= sprite.old_rect.bottom
                    ):
                        self.rect.top = sprite.rect.bottom

                    if (
                        self.rect.bottom >= sprite.rect.top
                        and self.old_rect.bottom <= sprite.old_rect.top
                    ):
                        self.rect.bottom = sprite.rect.top

                    self.dir.y = 0

    def update(self, dt: float):
        assert self.rect

        self.old_rect = self.rect.copy()

        self.action()
        self.move(dt)

        self.shoot_timer()

        self.image_index += 0.03
        self.image_index %= len(self.images[self.state])
        self.image = self.images[self.state][int(self.image_index)]

        if self.face_dir == -1:
            self._flip_face()

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= w_W:
            self.rect.right = w_W

        return True
