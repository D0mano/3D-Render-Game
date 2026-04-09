import random
import pygame
class Map:
    def __init__(self,game,col,row):
        self.game = game
        self.col = col
        self.row = row
        self.tile_map = self.create_random_tile_map()

    @property
    def screen(self):
        return self.game.screen

    @property
    def tile_size(self):
        return self.game.tile_size

    def is_wall(self, map_x, map_y):
        col, row = int(map_x // self.tile_size), int(map_y // self.tile_size)
        if not (0 <= row < self.row) or not (0 <= col < self.col):
            return True
        return self.tile_map[row][col] == 1


    def create_random_tile_map(self):
        tile_map = []
        for i in range(self.game.map_col):
            line = []
            for j in range(self.game.map_row):
                if i == 0 or i == self.game.map_col - 1 or j == 0 or j == self.game.map_row - 1:
                    line.append(1)
                else:
                    nb = random.randint(0, 4)
                    if nb == 0:
                        line.append(1)
                    else:
                        line.append(0)
            tile_map.append(line)
        return tile_map

    def draw(self):
        for y in range(self.row):
            for x in range(self.col):
                if self.tile_map[y][x] == 1:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)
                pygame.draw.rect(self.screen, color,
                                 (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))