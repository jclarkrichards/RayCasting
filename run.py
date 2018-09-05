import pygame
from pygame.locals import *
from vectors import *
from math import *
import numpy
from player import RayCaster
from mapper import Map
from line import Line
from tree_create_test import *

pygame.init()
W, H = 600,400
screen = pygame.display.set_mode((600, 400), 0, 32)
clock = pygame.time.Clock()
background = pygame.surface.Surface((W, H)).convert()
player = RayCaster(W,H)


lines = [Line(160,120,240,120), Line(240,120,240,200),
         Line(240,200,160,200), Line(160,200,160,120),
         Line(560,40,40,40), Line(560,360,560, 40),
         Line(40,360,560,360), Line(40,40,40,360)]

test = divideLines(lines)



walls = Map()
threeD = False

while True:
    dt = clock.tick(30) / 1000.0
    player.Move(dt)
    player.ResetRays()
    walls.TraverseTree(player, walls.tree)

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                threeD = not threeD

    if threeD:
        pygame.draw.rect(screen, (0,0,150), (0,0,W,H/2))
        pygame.draw.rect(screen, (116,90,10), (0,H/2, W, H/2))
        walls.Render3D(screen, player)
    else:
        screen.blit(background, (0,0))
        walls.renderWalls(screen)
        player.Render(screen)
        #player.RenderPointDirection(screen)
        player.RenderRays(screen)
    pygame.display.update()
