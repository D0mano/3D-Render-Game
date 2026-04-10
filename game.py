import pygame
import random

from map import Map
from player import Player
from ray_engine import RayEngine

class Game:
    FPS = 60
    def __init__(self):

        self.clock = pygame.time.Clock()
        self.map_col = 20
        self.map_row = 20
        self.map = Map(self,self.map_col,self.map_row)
        self.ray_engine = RayEngine(self)
        self.tile_original_size = 16
        self.scale = 3
        self.tile_size = self.tile_original_size * self.scale
        self.screen_size = self.map_col * self.tile_size, self.map_row * self.tile_size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.player = Player(self)
        self.running = True

    def is_wall(self, map_x, map_y):
        return self.map.is_wall(map_x, map_y)

    def draw(self):
        self.screen.fill((0,0,0))
        # self.map.draw()
        # self.player.draw()
        self.ray_engine.draw()

    def update(self):
        for event in pygame.event.get():
            self.handle_events(event)
        self.player.update()
        self.ray_engine.update()

    def display_tile_map(self):
        for row in self.map.tile_map:
            print(row)

    def handle_events(self,event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.map.tile_map = self.map.create_random_tile_map()
        self.player.handle_events(event)

    def run(self):
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
            pygame.display.update()



