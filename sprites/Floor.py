from settings import *

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, surf: pygame.Surface, groups) -> None:
        super().__init__(groups)
        
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        
        