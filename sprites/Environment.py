from settings import *
from sprites.RestrictedObject import RestrictedObject


class Environment(pygame.sprite.Sprite):
    def __init__(self, offset, groups):
        super().__init__(groups)

        self._groups = groups

        # signify the floor no (environment no)

        self.image = pygame.Surface(size=(w_W, 6 * t_H)).convert_alpha()
        self.image.fill((rand.randint(200, 255), 0, 0))

        self.rect = self.image.get_frect(
            topleft=(0, w_H - self.image.get_height() - offset * t_H)
        )

        self.floor = []
        self.make_floor()

        for section in self.floor:
            self.image.blit(section.image, section.rect)

        self.M = 10**13
        self.G = 6.673 * 10**-11

        self.b = vec(0, 0.82)
        self.kf = 0.2 - rand.randint(0, 10) / 100

        print("kf", self.kf)

        """
        1. Need a floor
        1.1. Floor will control, the kinetic friction and gravity (will increase as we go up)
        2. Need an atmosphere
        2.1. Atmosphere will control the air drag
        3. Do not create a separate atomsphere sprite. There will be floor sprite and the whole environment
        
        |``````````````````````|
        |      ATMOSPHERE      |
        |                      |
        |========FLOOR=========|
        """

    def make_floor(self):
        y = self.rect.bottom - t_H
        breakable_floor_width = rand.randint(5 * t_W, 6 * t_W)
        first_section_width = rand.randint(
            3 * t_W, int(self.rect.width - breakable_floor_width)
        )
        last_section_width = self.rect.width - (
            first_section_width + breakable_floor_width
        )

        if last_section_width < 0:
            last_section_width = 0

        floor_sections = [
            pygame.Rect(0, y, first_section_width, t_H),
            pygame.Rect(
                first_section_width + breakable_floor_width,
                y,
                last_section_width,
                t_H,
            ),
        ]

        for section in floor_sections:
            self.floor.append(
                RestrictedObject(
                    surf=pygame.Surface(size=(section.width, section.height)),
                    pos=vec(section.x, section.y),
                    groups=self._groups[0],
                    mass=100,
                )
            )
