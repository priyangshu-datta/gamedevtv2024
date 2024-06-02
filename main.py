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

        self.game_entities: pygame.sprite.Group = pygame.sprite.Group()
        self.floor_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.breakable_roof_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.enemy_sprites: pygame.sprite.Group = pygame.sprite.Group()

        self.player = Player(
            start_pos=(w_W - 40, 8 * w_H / 10),
            surf=pygame.Surface(size=(40, 60)),
            floors=self.floor_sprites,
            breakable_roofs=self.breakable_roof_sprites,
            enemies=self.enemy_sprites,
            groups=(self.game_entities,),
        )

        # self.zombie_spawn_event = pygame.event.custom_type()
        # self.zombie_spawn_timer = pygame.time.set_timer(self.zombie_spawn_event, )

        self.setup()

        # Zombie(
        #     base_floor=0,
        #     floors=self.floor_sprites,
        #     player=self.player,
        #     groups=(
        #         self.game_entities,
        #         self.enemy_sprites,
        #     ),
        # )

        self.font_renderer = pygame.Font(size=40)

        while self.running:
            self.run()

        pygame.quit()

    def setup(self):
        # world = tmx.load_pygame(Path("graphics/tiles/tmx/level_1.tmx").as_posix())

        for floor_no in range(4):
            y = w_H - (floor_no * 6 * t_H + t_H)

            """
            --------   ---------
            -------------   ----
            ---   --------------
            --------------------
            """
            
            breakable_floor_width = randint(5 * t_W, 6 * t_W)
            first_section_width = randint(3 * t_W, w_W - breakable_floor_width)
            last_section_width = w_W - (first_section_width + breakable_floor_width)
            
            if last_section_width < 0: last_section_width = 0

            floor_sections = [
                pygame.Rect(0, y, first_section_width, t_H),
                # pygame.Rect(first_section_width, y, breakable_floor_width, t_H),
                pygame.Rect(first_section_width + breakable_floor_width, y, last_section_width, t_H)
            ]
            
            for section in floor_sections:
                Floor(
                    pos=vec(section.x, section.y),
                    surf=pygame.Surface(size=(section.width, section.height)),
                    floor_no=floor_no,
                    groups=(self.game_entities, self.floor_sprites),
                )

            floor_no += 1

        # for obj in world.get_layer_by_name("Floors"):  # type: ignore

        #     Floor(
        #         pos=vec(x=obj.x, y=obj.y),
        #         surf=pygame.Surface(size=(obj.width, obj.height)),
        #         floor_no=obj.properties["floor_no"],
        #         groups=(self.game_entities, self.floor_sprites),
        #     )

        # for obj in world.get_layer_by_name("Breakable Roofs"):  # type: ignore
        #     Roof(
        #         vec(x=obj.x, y=obj.y),
        #         pygame.Surface(size=(obj.width, obj.height)),
        #         obj.properties["roof_no"],
        #         (self.game_entities, self.breakable_roof_sprites),
        #     )

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
                f"{(self.player.break_floor_buffer_time - pygame.time.get_ticks() + self.player.roof_broken_time)/1000:.0f}",
                False,
                "black",
            )
            self.rect = self.surf.get_frect(topright=(w_W, 0))
            self.display_surf.blit(self.surf, self.rect)

        # if len(self.enemy_sprites) < 5:
        #     Zombie(
        #         base_floor=0,
        #         floors=self.floor_sprites,
        #         player=self.player,
        #         groups=(
        #             self.game_entities,
        #             self.enemy_sprites,
        #         ),
        #     )
        if self.player.hp < 0:
            self.running = False

        self.game_entities.update(dt)
        self.game_entities.draw(self.display_surf)

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
