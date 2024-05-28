import pygame


class Collision(pygame.sprite.Sprite):
    def __init__(self, pos, surf: pygame.Surface, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        
    
    
