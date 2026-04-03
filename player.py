import pygame
import math
import utils

class Player:
    FOV = 60
    NUM_RAYS = 50

    def __init__(self,game):
        self.game = game
        self.rect = pygame.Rect(0,0, self.game.tile_size/2,self.game.tile_size/2)
        self.rect.center = (5 * self.game.tile_size ,5 * self.game.tile_size)

        self.angle = -math.pi/2                     #in rad
        self.direction: list[float] = [0.0, -1.0]
        self.angular_velocity = 0.05                #in rad/s
        self.velocity = 2                           #in px/s

        #   KEY FLAGS
        self.z_key_pressed = False
        self.q_key_pressed = False
        self.s_key_pressed = False
        self.d_key_pressed = False
    @property
    def row(self)->int:
        """
        :return: The row of the player
        """
        return self.rect.y // self.game.tile_size

    @property
    def col(self)->int:
        """
        :return: The column of the player
        """
        return self.rect.x // self.game.tile_size

    @property
    def x(self)->float:
        return self.rect.centerx
    @property
    def y(self)->float:
        return self.rect.centery


    def move(self,direction):
        """
        Move the player
        :param direction: 1 forward or -1 backward
        :return: None
        """
        self.rect.x = self.rect.x + direction * self.direction[0] * self.velocity
        self.rect.y = self.rect.y + direction * self.direction[1] * self.velocity

    def rotate(self,direction):
        """
        Rotate the player
        :param direction: For left : -1, For right : 1
        :return: None
        """

        self.angle = self.angle + direction * self.angular_velocity
        self.angle %= 2 * math.pi
        self.direction[0] = math.cos(self.angle)
        self.direction[1] = math.sin(self.angle)

    def update(self):
        if self.z_key_pressed:
            #self.rect.y -= self.velocity
            self.move(1)
        if self.s_key_pressed:
            #self.rect.y += self.velocity
            self.move(-1)
        if self.d_key_pressed:
            #self.rect.x += self.velocity
            self.rotate(1)
        if self.q_key_pressed:
            #self.rect.x -= self.velocity
            self.rotate(-1)

    def handle_events(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.z_key_pressed = True
            if event.key == pygame.K_s:
                self.s_key_pressed = True
            if event.key == pygame.K_d:
                self.d_key_pressed = True
            if event.key == pygame.K_q:
                self.q_key_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                self.z_key_pressed = False
            if event.key == pygame.K_s:
                self.s_key_pressed = False
            if event.key == pygame.K_d:
                self.d_key_pressed = False
            if event.key == pygame.K_q:
                self.q_key_pressed = False

    def draw(self):
        pygame.draw.rect(self.game.screen,(100,100,100),self.rect)
        self.draw_ray_casting()
        self.cast_ray(self.angle,(255,0,0))

    def cast_ray(self, angle, color=(255, 0, 0)):
        # HORIZONTAL CHEK
        found_horizontal_wall = False
        horizontal_hit_x = 0
        horizontal_hit_y = 0

        first_intersection_x = None
        first_intersection_y = None

        if math.sin(angle) < 0:
            first_intersection_y = (self.y // self.game.tile_size) * self.game.tile_size - 1
        else:
            first_intersection_y = ((self.y // self.game.tile_size) * self.game.tile_size) + self.game.tile_size

        first_intersection_x = self.x + (first_intersection_y - self.y) / math.tan(angle)

        next_horizontal_x = first_intersection_x
        next_horizontal_y = first_intersection_y

        ya = -self.game.tile_size if math.sin(angle) < 0 else self.game.tile_size
        xa = ya / math.tan(angle)
        while self.game.screen_size[0] >= next_horizontal_x >= 0 and self.game.screen_size[1] >= next_horizontal_y >= 0:
            if self.game.is_wall(next_horizontal_x, next_horizontal_y):
                found_horizontal_wall = True
                horizontal_hit_x , horizontal_hit_y = next_horizontal_x, next_horizontal_y
                break
            next_horizontal_x += xa
            next_horizontal_y += ya


        # VERTICAL CHECK
        found_vertical_wall = False
        vertical_hit_x = 0
        vertical_hit_y = 0
        if math.cos(angle) > 0:
            first_intersection_x = (self.x // self.game.tile_size) * self.game.tile_size + self.game.tile_size
        else:
            first_intersection_x = (self.x // self.game.tile_size) * self.game.tile_size - 1

        first_intersection_y = self.y + (first_intersection_x - self.x) * math.tan(angle)
        next_vertical_x = first_intersection_x
        next_vertical_y = first_intersection_y

        xa = self.game.tile_size if math.cos(angle) > 0 else -self.game.tile_size
        ya = xa * math.tan(angle)

        while self.game.screen_size[0] >= next_vertical_x >= 0 and self.game.screen_size[1] >= next_vertical_y >= 0:
            if self.game.is_wall(next_vertical_x, next_vertical_y):
                found_vertical_wall = True
                vertical_hit_x, vertical_hit_y = next_vertical_x, next_vertical_y
                break
            next_vertical_x += xa
            next_vertical_y += ya

        # DISTANCE CALCULATION
        horizontal_distance = utils.distance((self.x,self.y),(horizontal_hit_x,horizontal_hit_y)) if found_horizontal_wall else 99999
        vertical_distance = utils.distance((self.x,self.y),(vertical_hit_x,vertical_hit_y)) if found_vertical_wall else 99999

        if horizontal_distance < vertical_distance:
            pygame.draw.line(self.game.screen,(0,255,0),(self.x,self.y),(horizontal_hit_x,horizontal_hit_y))
        else:
            pygame.draw.line(self.game.screen, (0, 255, 0), (self.x, self.y), (vertical_hit_x, vertical_hit_y))



    def draw_ray_casting(self, fov=None):
        steps = 50
        fov = math.radians(self.FOV) if fov is None else math.radians(fov)
        angular_shift = fov / steps
        start_angle = self.angle - fov/2
        for step in range(steps):
            self.cast_ray(start_angle + step * angular_shift, (0, 255, 0))











