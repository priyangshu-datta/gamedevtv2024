from settings import *
from sprites.Bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos, surf, floors, breakable_roofs, enemies, groups):
        super().__init__(groups)

        self._groups = groups

        self.image = surf
        self.rect = self.image.get_frect(topleft=start_pos)

        self.image.fill("red")

        self.floors = floors
        self.enemies = enemies
        self.breakable_roofs = breakable_roofs

        self.prop_constant = 100

        # Changable constants
        self.air_friction = vec(0, 0.82)
        self.kinetic_friction = 0.2
        self.mass = 50
        self.gravity = 9.8
        self.min_speed = 0.01
        self.step_speed = 0.07
        self.max_speed = 3
        self.speed = 1

        # Physics variable
        self.last_v = 0
        self.last_pos = start_pos
        self.face_dir = 1
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, self.gravity)
        self.hp = 10

        # Surface contacts
        self.contact = {"f": False, "lw": False, "rw": False}
        self.broken_roof_no = -1
        self.max_active_floor = 0

        # Timers
        self.speed_increase_buffer_time = 2000
        self.speed_last_increase_time = pygame.time.get_ticks()

        self.shoot_last_time = pygame.time.get_ticks()
        self.shoot_buffer_time = 500

        self.break_floor_buffer_time = 5000
        self.roof_broken_time = float("inf")

    def check_floor(self):
        rect = self.rect
        player_bottom = pygame.FRect((rect.x, rect.bottom - 2), (rect.width, 2))
        player_top = pygame.FRect((rect.x, rect.y), (rect.width, 2))
        player_left = pygame.FRect(
            (rect.x, rect.y + rect.height / 4), (2, rect.height / 2)
        )
        player_right = pygame.FRect(
            (rect.x + rect.width, rect.y + rect.height / 4), (2, rect.height / 2)
        )

        if (
            self.broken_roof_no != -1
            and pygame.time.get_ticks() - self.roof_broken_time
            > self.break_floor_buffer_time
        ):
            [
                floor.kill()
                for floor in filter(
                    lambda floor: floor.floor_no == self.broken_roof_no,
                    self.floors.sprites(),
                )
            ]
            self.max_active_floor = self.broken_roof_no + 1
            self.broken_roof_no = -1

        for floor in self.floors:
            if floor.rect.colliderect(player_top):
                self.rect.top = floor.rect.bottom
                self.velocity.y = self.min_speed

            if floor.rect.colliderect(player_left):
                self.rect.left = floor.rect.right

            if floor.rect.colliderect(player_right):
                self.rect.right = floor.rect.left

            if floor.rect.colliderect(player_bottom):
                self.contact["f"] = True
                self.rect.bottom = floor.rect.top
                break

        else:
            self.contact["f"] = False

        for roof in self.breakable_roofs:
            if roof.rect.colliderect(player_top):
                self.rect.top = roof.rect.bottom
                self.velocity.y = self.min_speed

                roof.hp -= 1

                if roof.hp <= 0:
                    self.broken_roof_no = roof.roof_no
                    self.roof_broken_time = pygame.time.get_ticks()
                    roof.kill()

    def normal_force(self):
        if self.contact["f"]:
            self.acceleration.y = 0  # self.gravity - (normal_force := self.mass * self.gravity / self.mass)
            self.velocity.y = 0
            if self.velocity.x != 0:  # sliding friction
                self.acceleration.x = (
                    (-self.velocity.x / abs(self.velocity.x))
                    * self.kinetic_friction
                    * self.mass
                    * self.gravity
                )
            else:
                self.acceleration.x = 0
        else:
            if self.acceleration.y != 0:
                self.acceleration.y = self.gravity - (
                    drag_force := self.air_friction.y * self.velocity.y / self.mass
                )
            else:
                self.acceleration.y = self.gravity

            if abs(self.acceleration.y) < 10**-3:
                self.acceleration.y = 0

            self.acceleration.x = (
                0  # change this if need something like horizontal flying boost
            )

    def shoot(self):
        if pygame.time.get_ticks() - self.shoot_last_time > self.shoot_buffer_time:
            self.shoot_last_time = pygame.time.get_ticks()

            Bullet(
                self.rect.center,
                (self.face_dir * 100, 0),
                pygame.Surface(size=(10, 10)),
                self.enemies,
                self._groups,
            )

    def input(self):
        pressed_keys = pygame.key.get_pressed()
        released_keys = pygame.key.get_just_released()

        if released_keys[pygame.K_LEFT] or released_keys[pygame.K_RIGHT]:
            self.speed = self.min_speed

        if pressed_keys[pygame.K_f]:
            self.shoot()

        if not self.contact["f"]:
            return

        if pressed_keys[pygame.K_LEFT]:
            if (
                self.speed < self.max_speed
                and pygame.time.get_ticks() - self.speed_last_increase_time
                > self.speed_increase_buffer_time
            ):
                self.speed += self.step_speed

            self.velocity.x = -self.speed
            self.face_dir = -1

        if pressed_keys[pygame.K_RIGHT]:
            if (
                self.speed < self.max_speed
                and pygame.time.get_ticks() - self.speed_last_increase_time
                > self.speed_increase_buffer_time
            ):
                self.speed += self.step_speed

            self.velocity.x = self.speed
            self.face_dir = 1

        if pressed_keys[pygame.K_SPACE]:
            self.velocity.y = -7

    def sliding_friction(self):
        if (
            self.velocity.x * self.last_v.x < 0
            and abs(self.velocity.x - self.last_v.x) < 2
        ):
            self.velocity.x = 0
            self.acceleration.x = 0

    def keep_on_floor(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.face_dir = 1
            self.velocity.x = self.face_dir
        if self.rect.right > w_W:
            self.rect.right = w_W
            self.face_dir = -1
            self.velocity.x = self.face_dir

    def exit(self):
        if (
            self.rect.right < 0
            or self.rect.left > w_W
            or self.rect.top > w_H
            or self.rect.bottom < 0
        ):
            self.hp = -1

    def update(self, dt):
        self.keep_on_floor()

        self.last_pos = self.rect.topleft
        self.last_v = self.velocity.copy()

        self.input()
        self.check_floor()
        self.normal_force()

        if self.hp < 0:
            self.kill()

        self.velocity += 0.5 * self.acceleration * dt
        self.sliding_friction()
        self.rect.topleft += self.velocity * dt * self.prop_constant
        self.velocity += 0.5 * self.acceleration * dt

        self.exit()
