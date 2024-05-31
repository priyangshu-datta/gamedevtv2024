from settings import *

from random import randint
from sprites.Floor import Floor
from sprites.Player import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surf = pygame.display.set_mode((w_W, w_H))
        pygame.display.set_caption("MyGame")
        pygame.display.set_icon(pygame.image.load(Path("graphics/icon.jpg")))
        self.running = True
        self.clock = pygame.Clock()

        self.game_entites: pygame.sprite.Group = pygame.sprite.Group()
        self.floor_sprites: pygame.sprite.Group = pygame.sprite.Group()

        self.player = Player(
            start_pos=(w_W / 2, 0),
            surf=pygame.Surface(size=(40, 60)),
            floors=self.floor_sprites,
            groups=(self.game_entites,),
        )

        self.setup()

        while self.running:
            self.run()

        pygame.quit()

    def setup(self):
        world = tmx.load_pygame(Path("graphics/tiles/tmx/level_1.tmx").as_posix())

        for obj in world.get_layer_by_name("Floors"):  # type: ignore
            Floor(
                vec(x=obj.x, y=obj.y),
                pygame.Surface(size=(obj.width, obj.height)),
                (self.game_entites, self.floor_sprites),
            )

    def run(self) -> None:
        dt = self.clock.tick() / 1000  # in seconds
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
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
