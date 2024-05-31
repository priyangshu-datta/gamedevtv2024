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
        self.font_renderer = pygame.Font(size=20)

    def update(self, dt):
        self.image.fill("black")
        surf = self.font_renderer.render(f"HIT: {self.hp}", False, "white")
        rect = surf.get_frect(midright=(self.rect.width, self.rect.height / 2))

        self.image.blit(surf, rect)
