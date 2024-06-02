from settings import *


class RestrictedObject(pygame.sprite.Sprite):
    def __init__(self, surf: pygame.Surface, pos: vec, groups, mass):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

        # object properties
        self.M = mass
        self.x = pos

        # # movable but restricted objects
        # self.s = 0
        # self.v = vec(0, 0)
        # self.a = vec(0, 0)
