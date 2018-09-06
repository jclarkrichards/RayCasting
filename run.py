import pygame
from pygame.locals import *
from vectors import *
from math import *
from player import RayCaster
from mapper import Map

class GameRun(object):
    def __init__(self):
        pygame.init()
        self.W, self.H = 600,400
        screensize = (self.W, self.H)
        self.screen = pygame.display.set_mode(screensize, 0, 32)
        self.clock = pygame.time.Clock()
        self.background = pygame.surface.Surface(screensize).convert()

    def startGame(self):
        self.player = RayCaster(self.W, self.H)
        self.walls = Map()
        self.threeD = False

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.threeD = not self.threeD
        
    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.player.Move(dt)
        self.player.CheckCollision(self.walls.walls, self.screen)
        self.player.ResetRays()
        self.walls.TraverseTree(self.player, self.walls.tree)
        self.checkEvents()
        self.render()

    def drawFloor(self):
        pos = (0, self.H/2, self.W, self.H/2)
        pygame.draw.rect(self.screen, (116,90,10), pos)
        
    def drawCeiling(self):
        pos = (0, 0, self.W, self.H/2)
        pygame.draw.rect(self.screen, (10,0,150), pos)
        
    def render(self):
        if self.threeD:
            self.drawCeiling()
            self.drawFloor()
            self.walls.Render3D(self.screen, self.player)
        else:
            self.screen.blit(self.background, (0,0))
            self.walls.Render2D(self.screen)
            self.player.Render(self.screen)
            #player.RenderPointDirection(screen)
            self.player.RenderRays(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameRun()
    game.startGame()
    while True:
        game.update()
