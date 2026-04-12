import pygame
import math

import utils

class RayEngine:

    MAX_DEPTHS = 30
    RES  = 1

    def __init__(self,game):
        self.game = game
        self.NUM_RAYS = self.game.screen_size[0]
        self.FOV = self.player.FOV
        self.rays = [{} for _ in range(self.NUM_RAYS)]
        self.wall_img = pygame.image.load("wall.png")
        self.wall_img = pygame.transform.scale(self.wall_img,(self.game.tile_size,self.game.tile_size))

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
            if self.game.mode_3D:
                color = (255,255,255) if ray['side'] == 'vertical' else (160,160,160)
                line_height = (self.game.tile_size / ray['dist']) * 415

                draw_begin = (self.game.screen_size[1] / 2) - (line_height / 2) + self.player.horizon
                draw_end =  line_height

                img_col = self.get_texture_col(ray)
                img_col = pygame.transform.scale(img_col,(img_col.get_width(),line_height))
                self.game.screen.blit(img_col,(i*self.RES,draw_begin))

            if self.game.mode_2D:
                self.draw_2d_ray(ray,(0, 255, 0))
                self.draw_2d_ray(self.cast_ray(self.player.angle))

    def get_texture_col(self, ray):
        if ray['side'] == 'horizontal':
            # Sur un mur horizontal, la position sur la texture dépend de X
            offset = ray['hit'][0] % self.game.tile_size
        else:
            # Sur un mur vertical, elle dépend de Y
            offset = ray['hit'][1] % self.game.tile_size

        # Convertir l'offset en colonne de pixel dans la texture
        tex_x = int((offset / self.game.tile_size) * self.wall_img.get_width())
        tex_x = max(0, min(tex_x, self.wall_img.get_width() - self.RES))  # clamp

        rect = pygame.Rect(tex_x, 0, self.RES, self.wall_img.get_height())
        return self.wall_img.subsurface(rect)
