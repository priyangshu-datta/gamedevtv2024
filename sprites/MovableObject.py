from settings import *


class MovableObject(pygame.sprite.Sprite):
    def __init__(self, pos, m, v_i, a_i, environments, groups):
        super().__init__(groups)

        self.image = pygame.Surface(size=(30, 40))
        self.image.fill("blue")
        self.rect = self.image.get_frect(topleft=pos)

        self.prop_constant = 100

        # # environment variables (extract out to floor.py)
        self.envs = environments
        self.curr_env = None
        self.next_env = None
        self.kf = 0
        self.b = vec(0, 0)
        self.g = 0

        # # player properties
        # self.dim
        self.m = m
        self.x = vec(w_W / 2, 0)
        self.face_dir = 1
        self.min_s = 0.1
        self.step_s = 0.4
        self.max_s = 3
        self.s = self.min_s
        self.v = v_i
        self.a = a_i
        # self.environment

        self.contact = {"top": False, "bottom": False, "left": False, "right": False}

        """important to check if the force is kinetic friction, as the change in the direction of velocity may be due to other force and actually wanted. however, the change of direction in velocity due to kinetic friction is unwanted"""
        self.akf = False  # applying kinetic friction
        self.jump = False
        
        # timers
        self.speed_increase_buffer_time = 200
        self.speed_last_increase_time = pygame.time.get_ticks()

    def general_movement(self, dt):
        drag_force = self.b.elementwise() * self.v.elementwise()

        if self.contact["bottom"] and self.v.x != 0:
            contact_force = self.m * self.g
            frictional_force = vec(-self.face_dir * self.kf * contact_force, 0)
            self.akf = True
        else:
            frictional_force = vec(0, 0)

        a = round(self.a - drag_force / self.m + frictional_force / self.m, 3)
        # gravity always acts, contact force cancels gravity, any such modifications in parameters goes here;
        # created temp variable `a`, so that self.a is not modified
        if self.contact["bottom"] and not self.jump:
            a.y = 0
            self.v.y = 0

        if self.contact["top"]:
            self.v.y = 1

        if self.contact["left"]:
            self.v.x = 1

        if self.contact["right"]:
            self.v.x = -1

        self.v += round(0.5 * a * dt, 3)
        self.rect.topleft += round(self.v * dt * self.prop_constant, 3)
        self.v += round(0.5 * a * dt, 3)
        
        # stopping due to frictional force
        if (self.v.x + round(0.5 * a.x * dt, 3)) * self.v.x < 0 and self.akf:
            self.akf = False
            self.v.x = 0

    def keyboard_action(self):
        """
        use this function to move the object
        """

    def update_environment(self):
        lower_distance = float("inf")
        upper_distance = float("inf")
        for env in self.envs:
            if env.rect.bottom - t_H > self.rect.bottom:
                if lower_distance > env.rect.bottom - t_H - self.rect.bottom:
                    lower_distance = env.rect.bottom - t_H - self.rect.bottom
                    self.g = (
                        env.G
                        * env.M
                        * self.m
                        / (self.rect.centery - env.rect.centery) ** 2
                    )
                    self.b = env.b
                    self.kf = env.kf
                    self.curr_env = env

            if env.rect.bottom < self.rect.top:
                if upper_distance > env.rect.bottom - self.rect.top:
                    upper_distance = env.rect.bottom - self.rect.top
                    self.next_env = env

    def update(self, dt):
        # update environment
        self.update_environment()
        # change any kinetics parameter here, before calculation of new position
        self.keyboard_action()
        # calculate new position
        self.general_movement(dt)
        # restrict on floor
        object_bottom_rect = pygame.FRect(self.rect.bottomleft, (self.rect.width, 1))
        object_top_rect = pygame.FRect(self.rect.topleft, (self.rect.width, 1))
        object_left_rect = pygame.FRect(
            (self.rect.left, self.rect.top + 1.5) - vec(1, 0), (1, self.rect.height - 3)
        )
        object_right_rect = pygame.FRect(
            (self.rect.right, self.rect.top + 1.5), (1, self.rect.height - 3)
        )
        self.contact["bottom"] = (
            True
            if object_bottom_rect.collidelist([f.rect for f in self.curr_env.floor])
            >= 0
            else False
        )

        self.contact["top"] = (
            True
            if object_top_rect.collidelist([f.rect for f in self.next_env.floor]) >= 0
            else False
        )

        self.contact["left"] = (
            True
            if object_left_rect.collidelist([f.rect for f in self.next_env.floor]) >= 0
            or object_left_rect.collidelist([f.rect for f in self.curr_env.floor]) >= 0
            else False
        )

        self.contact["right"] = (
            True
            if object_right_rect.collidelist([f.rect for f in self.next_env.floor]) >= 0
            or object_right_rect.collidelist([f.rect for f in self.curr_env.floor]) >= 0
            else False
        )

        """
        kinetics of object will depened on velocity and acceleration only. change this properties appropiately
        
        
        ✅ always downward pull on object
        ✅ on floor contact downward pull neutrilizes
        ✅ in air, drag force slows down downward pull
        ✅ on floor kinetic friction slows down object+
        ✅ if no acceleration on object on floor, the speed decreases, at last stops
        """
