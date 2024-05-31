from settings import *

from random import randint
from sprites.Floor import Floor
from sprites.Roof import Roof
from sprites.Player import Player
from sprites.Zombie import Zombie


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
        self.breakable_roof_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.enemy_sprites: pygame.sprite.Group = pygame.sprite.Group()

        self.player = Player(
            start_pos=(w_W - 40, 8 * w_H / 10),
            surf=pygame.Surface(size=(40, 60)),
            floors=self.floor_sprites,
            breakable_roofs=self.breakable_roof_sprites,
            enemies=self.enemy_sprites,
            groups=(self.game_entites,),
        )

        # self.zombie_spawn_event = pygame.event.custom_type()
        # self.zombie_spawn_timer = pygame.time.set_timer(self.zombie_spawn_event, )

        self.setup()

        for _ in range(5):
            Zombie(
                start_pos=(
                    randint(50, w_W - 500),
                    list(
                        filter(
                            lambda floor: floor.floor_no == 0,
                            self.floor_sprites.sprites(),
                        )
                    )[0].rect.top
                    - 60,
                ),
                surf=pygame.Surface(size=(40, randint(40, 60))),
                floors=self.floor_sprites,
                breakable_floors=self.breakable_roof_sprites,
                player=self.player,
                groups=(self.game_entites, self.enemy_sprites),
            )

        self.font_renderer = pygame.Font(size=40)

        while self.running:
            self.run()

        pygame.quit()

    def setup(self):
        world = tmx.load_pygame(Path("graphics/tiles/tmx/level_1.tmx").as_posix())

        for obj in world.get_layer_by_name("Floors"):  # type: ignore
            Floor(
                vec(x=obj.x, y=obj.y),
                pygame.Surface(size=(obj.width, obj.height)),
                obj.properties["floor_no"],
                (self.game_entites, self.floor_sprites),
            )

        for obj in world.get_layer_by_name("Breakable Roofs"):  # type: ignore
            Roof(
                vec(x=obj.x, y=obj.y),
                pygame.Surface(size=(obj.width, obj.height)),
                obj.properties["roof_no"],
                (self.game_entites, self.breakable_roof_sprites),
            )

    def run(self) -> None:
        dt = self.clock.tick() / 1000  # in seconds
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        self.display_surf.fill("white")

        self.surf = self.font_renderer.render(
            f"HP: {self.player.hp:.2f}", False, "black"
        )
        self.rect = self.surf.get_frect(midtop=(w_W / 2, 0))
        self.display_surf.blit(self.surf, self.rect)

        if self.player.broken_roof_no != -1:

            self.surf = self.font_renderer.render(
                f"{(pygame.time.get_ticks() - self.player.roof_broken_time)/1000:.0f}",
                False,
                "black",
            )
            self.rect = self.surf.get_frect(topright=(w_W, 0))
            self.display_surf.blit(self.surf, self.rect)

        if len(self.enemy_sprites) < 5:
            Zombie(
                start_pos=(
                    randint(0, w_W),
                    list(
                        filter(
                            lambda floor: floor.floor_no
                            == self.player.standing_floor_no,
                            self.floor_sprites.sprites(),
                        )
                    )[0].rect.y
                    - 200,
                ),
                surf=pygame.Surface(size=(40, randint(40, 60))),
                floors=self.floor_sprites,
                breakable_floors=self.breakable_roof_sprites,
                player=self.player,
                groups=(self.game_entites, self.enemy_sprites),
            )

        if self.player.hp < 0:
            self.running = False

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
