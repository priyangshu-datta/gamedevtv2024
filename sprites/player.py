from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos, surf, floors, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft=start_pos)

        self.image.fill("red")

        self.floors = floors

        self.prop_constant = 100

        # Changable constants
        self.air_friction = vec(0, 0.82)
        self.kinetic_friction = 0.2
        self.mass = 50
        self.gravity = 9.8
        self.min_speed = 0.008
        self.step_speed = 0.02
        self.max_speed = 3
        self.speed = 1

        # Physics variable
        self.last_v = 0
        self.last_pos = start_pos
        self.displacement = 0
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, self.gravity)

        # Surface contacts
        self.contact = {"f": False, "lw": False, "rw": False}

        # Timers
        self.speed_increase_buffer_time = 2000
        self.speed_last_increase_time = pygame.time.get_ticks()

    def check_floor(self):
        # floor_rects = [floor.rect for floor in self.floors]
        # self.contact["f"] = True if self.rect.collidelist(floor_rects) >= 0 else False
        rect = self.rect
        player_bottom = pygame.FRect(rect.bottomleft, (rect.width, 2))
        player_top = pygame.FRect((rect.x, rect.y), (rect.width, 2))

        for floor in self.floors:
            if floor.rect.colliderect(player_top):
                self.rect.top = floor.rect.bottom
                self.velocity.y = self.min_speed
            if floor.rect.colliderect(self.rect):
                self.contact["f"] = True
                self.rect.bottom = floor.rect.top
                break

        else:
            self.contact["f"] = False

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

    def input(self):
        pressed_keys = pygame.key.get_pressed()
        released_keys = pygame.key.get_just_released()

        if released_keys[pygame.K_LEFT] or released_keys[pygame.K_RIGHT]:
            self.speed = self.min_speed

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

        if pressed_keys[pygame.K_RIGHT]:
            if (
                self.speed < self.max_speed
                and pygame.time.get_ticks() - self.speed_last_increase_time
                > self.speed_increase_buffer_time
            ):
                self.speed += self.step_speed

            self.velocity.x = self.speed

        if pressed_keys[pygame.K_SPACE]:
            self.velocity.y = -7

    def sliding_friction(self):
        if (
            self.velocity.x * self.last_v.x < 0
            and abs(self.velocity.x - self.last_v.x) < 2
        ):
            self.velocity.x = 0
            self.acceleration.x = 0

    def update(self, dt):
        self.last_pos = self.rect.topleft
        self.last_v = self.velocity.copy()

        self.input()
        self.check_floor()
        self.normal_force()

        self.velocity += 0.5 * self.acceleration * dt
        self.sliding_friction()
        self.rect.topleft += self.velocity * dt * self.prop_constant
        self.velocity += 0.5 * self.acceleration * dt

        self.displacement = vec(self.rect.topleft) - vec(self.last_pos)
