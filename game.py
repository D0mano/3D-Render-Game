import pygame
import random

from player import Player


class Game:
    FPS = 60
    def __init__(self):

        self.clock = pygame.time.Clock()

        self.map_col = 10
        self.map_row = 10
        self.tile_original_size = 16
        self.scale = 3
        self.tile_size = self.tile_original_size * self.scale
        self.screen_size = self.map_col * self.tile_size, self.map_row * self.tile_size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.tile_map = self.create_random_tile_map()

        self.player = Player(self)
        self.running = True







    def draw_tile_map(self):
        for y in range(self.map_row):
            for x in range(self.map_col):
                if self.tile_map[x][y] == 1:
                    color = (255,255,255)
                else:
                    color = (0,0,0)
                pygame.draw.rect(self.screen,color,(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))

    def draw(self):
        self.draw_tile_map()
        self.player.draw()

    def update(self):
        for event in pygame.event.get():
            self.handle_events(event)
        self.player.update()


    def create_random_tile_map(self):
        tile_map = []
        for _ in range(self.map_col):
            line = []
            for _ in range(self.map_row):
                nb = random.randint(0, 4)
                if nb == 0:
                    line.append(1)
                else:
                    line.append(0)
            tile_map.append(line)
        return tile_map

    def display_tile_map(self):
        for row in self.tile_map:
            print(row)

    def handle_events(self,event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.tile_map = self.create_random_tile_map()
        self.player.handle_events(event)

    def run(self):
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
            pygame.display.update()



