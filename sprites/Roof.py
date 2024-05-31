from settings import *


class Roof(pygame.sprite.Sprite):
    def __init__(
        self, pos: pygame.Vector2, surf: pygame.Surface, roof_no: int, groups
    ) -> None:
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.hp = 5
        self.roof_no = roof_no
