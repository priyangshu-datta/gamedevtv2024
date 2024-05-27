from settings import *

from sprites.player import Player
from sprites.drone import Drone


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surf = pygame.display.set_mode((w_W, w_H))
        pygame.display.set_caption("MyGame")
        pygame.display.set_icon(pygame.image.load("graphics/icon.jpg"))
        self.running = True
        self.clock = pygame.Clock()

        self.game_entites = pygame.sprite.Group()
        self.player = Player(self.game_entites)
        self.drone = Drone(self.game_entites, self.player)

        while self.running:
            self.run()

        pygame.quit()

    def run(self) -> None:
        dt = self.clock.tick() / 1000  # in seconds
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        if pygame.sprite.collide_mask(self.player, self.drone):
            self.running = False

        self.display_surf.fill("white")

        self.game_entites.update(dt)
        self.game_entites.draw(self.display_surf)

        pygame.display.update()


def main():
    Game()


if __name__ == "__main__":
    main()


"""

1000 fr / s := 1000 images per second
100 px / fr
0.001 Hz := deltatime
100 * 0.001 := 0.1 px / fr
0.1 px / fr * 1000 fr / s := 100 px / s

I want the speed to be 100 px/s. I know 1000 frames are generated in 1s, i.e., 1000 fr/s. Then I want 100 px/s * 0.001 s/fr = 0.1 px/fr, i.e., i want 
0.1 px movement per frame. Now, dt = 0.001 s/fr, v = 100 px/s. Then we get what we have to show to the screen, that is 0.1 px/fr.

I want the speed to be `v` px/s. I know `f` frames are generated in 1s, i.e., `f` fr/s. Then I want `v` px/s * (1/`f`) s/fr = `v`/`f` px/fr, 
i.e., i want `v`/`f` px movement per frame. Now, `dt` = (1/`f`) s/fr. Then we get what we have to show to the screen, that is `v`/`f` px/fr.

"""
