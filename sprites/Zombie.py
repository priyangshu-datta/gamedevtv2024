from settings import *
import random
from sprites.MovableObject import MovableObject

# class Zombie(pygame.sprite.Sprite):
#     def __init__(self, base_floor, floors, player, groups):
#         super().__init__(groups)

#         self.base_floor = base_floor
#         allowed_spawing_area = [
#             floor.rect
#             for floor in filter(lambda floor: floor.floor_no == self.base_floor, floors)
#         ]

#         self.floor_section = random.choices(
#             allowed_spawing_area,
#             [area.width for area in allowed_spawing_area],
#             k=1,
#         )[0]

#         start_pos = vec(
#             random.randint(
#                 int(self.floor_section.x),
#                 int(
#                     self.floor_section.x + self.floor_section.width
#                     if self.base_floor != 0
#                     else self.floor_section.width - 400
#                 ),
#             ),
#             self.floor_section.y,
#         )

#         self.image = pygame.Surface(size=(40, self.floor_section.height * 2))
#         self.rect = self.image.get_frect(topleft=start_pos)

#         self.image.fill(
#             (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#         )

#         self.prop_constant = 100
#         self.floors = floors
#         self.player = player

#         # Changable constants
#         self.air_friction = vec(0, 0.82)
#         self.kinetic_friction = 0.2
#         self.mass = 50
#         self.gravity = 0.8
#         self.min_speed = 0.008
#         self.step_speed = 0.02
#         self.max_speed = 3
#         self.speed = self.min_speed + random.random() * self.max_speed

#         # Physics variable
#         self.last_v = vec(0, 0)
#         self.last_pos = self.rect.topleft
#         self.face_dir = 1
#         self.velocity = vec(1, -3)
#         self.acceleration = vec(10, self.gravity)

#         self.contact = {"f": False, "lw": False, "rw": False}

#         self.hp = 5

#         # timers
#         self.last_attack_time = pygame.time.get_ticks()
#         self.attack_dur = 200

#     def check_floor(self):
#         rect = self.rect
#         zombie_bottom = pygame.FRect((rect.x, rect.bottom - 2), (rect.width, 2))
#         zombie_top = pygame.FRect((rect.x, rect.y), (rect.width, 2))
#         zombie_left = pygame.FRect(
#             (rect.x, rect.y + rect.height / 4), (2, rect.height / 2)
#         )
#         zombie_right = pygame.FRect(
#             (rect.x + rect.width, rect.y + rect.height / 4), (2, rect.height / 2)
#         )

#         for floor in self.floors:
#             if floor.rect.colliderect(zombie_top):
#                 self.rect.top = floor.rect.bottom
#                 self.velocity.y = -4

#             if floor.rect.colliderect(zombie_left):
#                 self.rect.left = floor.rect.right

#             if floor.rect.colliderect(zombie_right):
#                 self.rect.right = floor.rect.left

#             if floor.rect.colliderect(zombie_bottom):
#                 self.contact["f"] = True
#                 self.rect.bottom = floor.rect.top
#                 break
#         else:
#             self.contact["f"] = False

#     def player_collision(self):
#         rect = self.player.rect
#         player_bottom = pygame.FRect(rect.bottomleft, (rect.width, 2))
#         player_top = pygame.FRect((rect.x, rect.y), (rect.width, 2))
#         player_left = pygame.FRect(
#             (rect.x, rect.y + rect.height / 4), (2, rect.height / 2)
#         )
#         player_right = pygame.FRect(
#             (rect.x + rect.width, rect.y + rect.height / 4), (2, rect.height / 2)
#         )

#         if self.rect.colliderect(player_left):
#             self.player.left = self.rect.right

#         if self.rect.colliderect(player_right):
#             self.player.right = self.rect.left

#         if (
#             self.rect.colliderect(rect)
#             and pygame.time.get_ticks() - self.last_attack_time > self.attack_dur
#         ):
#             self.last_attack_time = pygame.time.get_ticks()
#             self.velocity.x = -self.face_dir * 2
#             self.player.hp -= 0.4

#         if (
#             pygame.time.get_ticks() - self.last_attack_time < 300
#             and pygame.time.get_ticks() - self.last_attack_time > self.attack_dur
#         ):
#             self.velocity.x = self.face_dir

#     def normal_force(self):
#         if self.contact["f"]:
#             self.acceleration.y = 0  # self.gravity - (normal_force := self.mass * self.gravity / self.mass)
#             self.velocity.y = 0
#         else:
#             if self.acceleration.y != 0:
#                 self.acceleration.y = self.gravity - (
#                     drag_force := self.air_friction.y * self.velocity.y / self.mass
#                 )
#             else:
#                 self.acceleration.y = self.gravity

#             if abs(self.acceleration.y) < 10**-3:
#                 self.acceleration.y = 0

#             self.acceleration.x = (
#                 0  # change this if need something like horizontal flying boost
#             )

#     def sliding_friction(self):
#         if (
#             self.velocity.x * self.last_v.x < 0
#             and abs(self.velocity.x - self.last_v.x) < 2
#         ):
#             self.velocity.x = 0
#             self.acceleration.x = 0

#     def exit(self):
#         if (
#             self.rect.right < 0
#             or self.rect.left > w_W
#             or self.rect.top > w_H
#             or self.rect.bottom < 0
#         ):
#             self.kill()

#     def keep_on_floor(self):
#         if self.rect.left < 0:
#             self.rect.left = 0
#             self.face_dir = 1
#             self.velocity.x = self.face_dir
#         if self.rect.right > w_W:
#             self.rect.right = w_W
#             self.face_dir = -1
#             self.velocity.x = self.face_dir

#     def update(self, dt):
#         self.keep_on_floor()
#         self.player_collision()

#         self.last_pos = self.rect.topleft
#         self.last_v = self.velocity.copy()

#         self.check_floor()
#         self.normal_force()

#         if self.hp < 0:
#             self.kill()

#         self.velocity += 0.5 * self.acceleration * dt
#         self.sliding_friction()
#         self.rect.topleft += self.velocity * dt * self.prop_constant
#         self.velocity += 0.5 * self.acceleration * dt

#         self.displacement = vec(self.rect.topleft) - vec(self.last_pos)

#         # self.exit()


class Zombie(MovableObject):
    def __init__(self, groups):
        super().__init__(
            pos=vec(0, w_H),
            m=20,
            v_i=vec(2, 0),
            a_i=vec(9.8 * 0.08, 9.8),
            groups=groups,
        )
