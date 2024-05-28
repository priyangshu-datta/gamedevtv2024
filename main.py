from settings import *

from sprites.player import Player
from sprites.drone import Drone
from sprites.world import World
from sprites.collision import Collision
from random import randint


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surf = pygame.display.set_mode((w_W, w_H))
        pygame.display.set_caption("MyGame")
        pygame.display.set_icon(pygame.image.load(Path("graphics/icon.jpg")))
        self.running = True
        self.clock = pygame.Clock()

        self.game_entites = pygame.sprite.Group()
        self.collision_sprities = pygame.sprite.Group()

        self.player = Player((self.game_entites,), self.collision_sprities)
        self.drone = Drone(
            self.player,
            (d_pos := pygame.Vector2((randint(0, w_W), 0))),
            (pygame.Vector2(self.player.rect.center) - d_pos).normalize(),  # type: ignore
            (self.game_entites, self.collision_sprities),
        )

        self.setup()

        while self.running:
            self.run()

        pygame.quit()

    def setup(self):
        world = tmx.load_pygame(Path("graphics/tiles/tmx/level_1.tmx").as_posix())

        # for obj in world.get_layer_by_name("Collision"):  # type: ignore
        #     Collision(
        #         (obj.x, obj.y),
        #         pygame.Surface((obj.width, obj.height)),
        #         self.game_entites,
        #     )
        for x, y, image in world.get_layer_by_name("Level 1").tiles():  # type: ignore
            World((x * 32, y * 32), image, (self.game_entites, self.collision_sprities))

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
