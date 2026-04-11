import pygame

from ray_engine import RayEngine


class Renderer:
    def __init__(self, game):
        self.game = game
        self.ray_engine = RayEngine(game)
        self.screen = self.game.screen
        self.screen_size = self.screen.get_size()
        self.player = self.ray_engine.player

    def draw(self):
        self.draw_background()
        self.ray_engine.draw()

    def update(self):
        self.ray_engine.update()

    def draw_background(self):
        pygame.draw.rect(self.screen,(202, 240, 248),(0,0,self.screen_size[0],self.screen_size[1]/2 + self.player.horizon))
        pygame.draw.rect(self.screen,(43, 147, 72),(0,self.screen_size[1]/2 + self.player.horizon,self.screen_size[0],self.screen_size[1]/2 - self.player.horizon))

