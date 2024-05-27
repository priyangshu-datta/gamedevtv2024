import pygame
from settings import w_W, w_H
from pathlib import Path
from enum import StrEnum, auto, Enum
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
    def __init__(self, groups):
        super().__init__(groups)
        self.groups = groups
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
        self.dir = pygame.Vector2(1, 0)
        self.image = self.images[self.state][self.image_index]
        self.rect = self.image.get_frect(center=(w_W / 2, w_H - 80))
        self.speed = 500
        self.gravity = 1.4
        self.jumping = False
        self.base = w_H - 80
        self.jump_height = 220
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
        if self.dir.x == -1:
            bullet_start_pos = pygame.Vector2(
                self.rect.midleft[0], self.rect.midleft[1]
            )
        else:
            bullet_start_pos = pygame.Vector2(
                self.rect.midright[0], self.rect.midright[1]
            )

        bullet_start_pos += (bullet_start_pos - self.rect.midtop) / 2
        Bullet(self.groups, bullet_start_pos, self.dir.x)

    def jump(self):
        assert self.rect
        if not self.jumping:
            self.jumping = True
            self.state = PlayerState.JUMPING
            self.dir.y = -1

    def action(self, dt: float):
        keys = pygame.key.get_pressed()

        if not any([keys[action_key] for action_key in self.actions]):
            self.state = PlayerState.IDLE
            return

        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.state = PlayerState.RUNNING
            self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            assert self.rect
            self.rect.center += self.dir * self.speed * dt
            
            
        if keys[pygame.K_UP]:
            self.jump()
            
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def update(self, dt: float):
        
        self.action(dt)

        self.shoot_timer()

        self.image_index += 0.03
        self.image_index %= len(self.images[self.state])
        self.image = self.images[self.state][int(self.image_index)]

        if self.dir.x == -1:
            self._flip_face()

        assert self.rect
        if self.jumping:
            self.rect.centery += self.dir.y * self.gravity * self.speed * dt

        if self.rect.centery > self.base:
            self.rect.centery = self.base
            self.jumping = False
            self.state = PlayerState.IDLE

        if self.rect.centery <= self.base - self.jump_height:
            self.dir.y = 1

        if self.rect.bottom >= w_H:
            self.rect.bottom = w_H
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= w_W:
            self.rect.right = w_W
            
        return True
