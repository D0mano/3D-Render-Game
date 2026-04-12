import pygame
import random

from map import Map
from player import Player
from renderer import Renderer

class Game:
    FPS = 60
    def __init__(self):

        self.clock = pygame.time.Clock()
        self.map_col = 11
        self.map_row = 11
        self.map = Map(self,self.map_col,self.map_row)
        self.tile_original_size = 16
        self.scale = 5
        self.tile_size = self.tile_original_size * self.scale
        self.screen_size = self.map_col * self.tile_size, self.map_row * self.tile_size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.player = Player(self)
        self.running = True

        self.renderer = Renderer(self)

        self.mode_2D = False
        self.mode_3D = True



    def is_wall(self, map_x, map_y):
        return self.map.is_wall(map_x, map_y)

    def draw(self):
        self.renderer.draw()
        if self.mode_2D:
            self.map.draw()
            self.player.draw()

    def update(self):
        for event in pygame.event.get():
            self.handle_events(event)
        self.player.update()
        self.renderer.update()

    def display_tile_map(self):
        for row in self.map.tile_map:
            print(row)

    def handle_events(self,event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.map.tile_map = self.map.create_random_tile_map()
            if event.key == pygame.K_ESCAPE:
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)

        self.player.handle_events(event)

    def run(self):
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
            pygame.display.update()



