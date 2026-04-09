import pygame
import math

import utils

class RayEngine:
    FOV = 60
    NUM_RAYS = 50
    MAX_DEPTHS = 30

    def __init__(self,game):
        self.game = game
        self.rays = [{} for _ in range(self.NUM_RAYS)]
    @property
    def player(self):
        return self.game.player
    @property
    def map(self):
        return self.game.map

    def update(self):
        self.update_ray_casting()


    def update_ray_casting(self,fov=None):
        fov = math.radians(self.FOV) if fov is None else math.radians(fov)
        angular_shift = fov / self.NUM_RAYS
        start_angle = self.player.angle - fov / 2
        for step in range(self.NUM_RAYS):
            ray = self.cast_ray(start_angle + step * angular_shift)
            self.rays[step] = ray

    def cast_ray(self, angle):
        # HORIZONTAL CHEK
        if math.sin(angle) < 0:
            first_intersection_y = (self.player.y // self.game.tile_size) * self.game.tile_size - 1
        else:
            first_intersection_y = ((self.player.y // self.game.tile_size) * self.game.tile_size) + self.game.tile_size

        first_intersection_x = self.player.x + (first_intersection_y - self.player.y) / math.tan(angle)

        next_horizontal_x = first_intersection_x
        next_horizontal_y = first_intersection_y

        ya = -self.game.tile_size if math.sin(angle) < 0 else self.game.tile_size
        xa = ya / math.tan(angle)

        while not self.game.is_wall(next_horizontal_x, next_horizontal_y) :
            next_horizontal_x += xa
            next_horizontal_y += ya
        horizontal_hit = next_horizontal_x, next_horizontal_y


        # VERTICAL CHECK
        if math.cos(angle) > 0:
            first_intersection_x = (self.player.x // self.game.tile_size) * self.game.tile_size + self.game.tile_size
        else:
            first_intersection_x = (self.player.x // self.game.tile_size) * self.game.tile_size - 1

        first_intersection_y = self.player.y + (first_intersection_x - self.player.x) * math.tan(angle)
        next_vertical_x = first_intersection_x
        next_vertical_y = first_intersection_y

        xa = self.game.tile_size if math.cos(angle) > 0 else -self.game.tile_size
        ya = xa * math.tan(angle)

        while not self.game.is_wall(next_vertical_x, next_vertical_y) :
            next_vertical_x += xa
            next_vertical_y += ya
        vertical_hit = next_vertical_x, next_vertical_y


        # DISTANCE CALCULATION
        horizontal_distance = utils.distance((self.player.x,self.player.y),horizontal_hit)
        vertical_distance = utils.distance((self.player.x,self.player.y),vertical_hit )

        if horizontal_distance < vertical_distance:
            return {'dist':horizontal_distance,'hit':horizontal_hit,'side':'horizontal'}
        else:
            return {'dist':vertical_distance,'hit':vertical_hit,'side':'vertical'}

    def draw_2d_ray(self,ray_result,color=(255,0,0)):
        """Draw a ray in a top-down view using the cast_ray functions"""
        if ray_result['hit'] is None:
            return
        pygame.draw.line(self.game.screen,color,(self.player.x,self.player.y),ray_result['hit'])

    def draw_ray_casting(self):
        for ray in self.rays:
            self.draw_2d_ray(ray,(0, 255, 0))
        self.draw_2d_ray(self.cast_ray(self.player.angle))