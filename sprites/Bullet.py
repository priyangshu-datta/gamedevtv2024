from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, acceleration, surf, enemy_sprites, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft=start_pos)

        self.image.fill("green")

        self.enemies = enemy_sprites

        self.prop_constant = 100

        self.velocity = vec(0, 0)
        self.acceleration = vec(acceleration)

    def enemy_hit(self):
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.rect):
                enemy.hp -= 1
                self.kill()

    def exit(self):
        if (
            self.rect.left < 0
            or self.rect.right > w_W
            or self.rect.top > w_H
            or self.rect.bottom < 0
        ):
            self.kill()

    def update(self, dt):
        self.velocity += 0.5 * self.acceleration * dt
        self.rect.topleft += self.velocity * dt * self.prop_constant
        self.velocity += 0.5 * self.acceleration * dt

        self.enemy_hit()
        self.exit()
