import pygame
import math

import utils

class RayEngine:
    FOV = 60
    MAX_DEPTHS = 30
    RES  = 1

    def __init__(self,game):
        self.game = game
        self.NUM_RAYS = self.game.screen_size[0]
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
        epsilon = 0.0001
        # HORIZONTAL CHEK
        if math.sin(angle) < 0: # going up
            first_intersection_y = (self.player.y // self.game.tile_size) * self.game.tile_size
            check_y = -epsilon
        else: # going down
            first_intersection_y = ((self.player.y // self.game.tile_size) * self.game.tile_size) + self.game.tile_size
            check_y = epsilon

        first_intersection_x = self.player.x + (first_intersection_y - self.player.y) / math.tan(angle)

        next_horizontal_x = first_intersection_x
        next_horizontal_y = first_intersection_y

        ya = -self.game.tile_size if math.sin(angle) < 0 else self.game.tile_size
        xa = ya / math.tan(angle)

        while not self.game.is_wall(next_horizontal_x, next_horizontal_y + check_y) :
            next_horizontal_x += xa
            next_horizontal_y += ya
        horizontal_hit = next_horizontal_x, next_horizontal_y


        # VERTICAL CHECK
        if math.cos(angle) > 0: # We are going right
            first_intersection_x = (self.player.x // self.game.tile_size) * self.game.tile_size + self.game.tile_size
            check_x = epsilon
        else:
            first_intersection_x = (self.player.x // self.game.tile_size) * self.game.tile_size
            check_x = -epsilon

        first_intersection_y = self.player.y + (first_intersection_x - self.player.x) * math.tan(angle)
        next_vertical_x = first_intersection_x
        next_vertical_y = first_intersection_y

        xa = self.game.tile_size if math.cos(angle) > 0 else -self.game.tile_size
        ya = xa * math.tan(angle)

        while not self.game.is_wall(next_vertical_x + check_x, next_vertical_y) :
            next_vertical_x += xa
            next_vertical_y += ya
        vertical_hit = next_vertical_x, next_vertical_y


        # DISTANCE CALCULATION
        horizontal_distance = utils.distance((self.player.x,self.player.y),horizontal_hit)
        vertical_distance = utils.distance((self.player.x,self.player.y),vertical_hit )

        if horizontal_distance < vertical_distance:
            horizontal_distance = round(horizontal_distance *math.cos(angle - self.player.angle),2)
            return {'dist':horizontal_distance,'hit':horizontal_hit,'side':'horizontal'}
        else:
            vertical_distance = round(vertical_distance * math.cos(angle - self.player.angle),2)
            return {'dist':vertical_distance,'hit':vertical_hit,'side':'vertical'}

    def draw_2d_ray(self,ray_result,color=(255,0,0)):
        """Draw a ray in a top-down view using the cast_ray functions"""
        if ray_result['hit'] is None:
            return
        pygame.draw.line(self.game.screen,color,(self.player.x,self.player.y),ray_result['hit'])

    def draw(self):
        for i,ray in enumerate(self.rays):

            # self.draw_2d_ray(ray,(0, 255, 0))


            color = (255,255,255) if ray['side'] == 'vertical' else (160,160,160)
            line_height = (self.game.tile_size / ray['dist']) * 415

            draw_begin = (self.game.screen_size[1] / 2) - (line_height / 2)
            draw_end =  line_height

            pygame.draw.rect(self.game.screen,color,(i*self.RES,draw_begin,self.RES,draw_end))
        self.draw_2d_ray(self.cast_ray(self.player.angle))