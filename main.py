import pygame
from settings import *

pygame.init()
display_surf = pygame.display.set_mode((w_W, w_H))
pygame.display.set_caption("MyGame")
pygame.display.set_icon(pygame.image.load("graphics/icon.jpg"))
running = True
timer = pygame.Clock()


import time

from sprites.player import Player
from sprites.drone import Drone

player_group = pygame.sprite.Group()
player = Player(player_group)
drone = Drone(player_group, player)

while running:
    dt = timer.tick() / 1000  # restricts generation of 120 images per second

    start = time.perf_counter()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    display_surf.fill("white")

    player_group.update(dt)
    player_group.draw(display_surf)

    pygame.display.update()


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


pygame.quit()
