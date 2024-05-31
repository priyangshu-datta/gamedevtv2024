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
        self.max_speed = 1

        # Physics variable
        self.last_v = 0
        self.last_pos = start_pos
        self.displacement = 0
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, self.gravity)

        # urface contacts
        self.contact = {"f": False, "lw": False, "rw": False}

    def check_floor(self):
        floor_rects = [floor.rect for floor in self.floors]
        self.contact["f"] = True if self.rect.collidelist(floor_rects) >= 0 else False

        for floor in self.floors:
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
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            # impulse
            self.velocity.x = -self.max_speed

        if keys[pygame.K_RIGHT]:
            # impulse
            self.velocity.x = self.max_speed

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
