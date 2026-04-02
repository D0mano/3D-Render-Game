import pygame

import math

class Player:
    def __init__(self,game):
        self.game = game
        self.row = 5
        self.col = 5

        self.x = self.row * self.game.tile_size
        self.y = self.col * self.game.tile_size

        self.rect = pygame.Rect(0,0, self.game.tile_size/2,self.game.tile_size/2)
        self.rect.center = (self.x, self.y)

        self.angle = -math.pi/2          #in rad
        self.direction = [0,-1]
        self.angular_velocity = 0.05       #in rad/s
        self.velocity = 2              #in px/s

        #   KEY FLAGS
        self.z_key_pressed = False
        self.q_key_pressed = False
        self.s_key_pressed = False
        self.d_key_pressed = False

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
        :param direction: 1 for left, -1 for right
        :return: None
        """

        self.angle = self.angle + direction * self.angular_velocity
        self.direction[0] = math.cos(self.angle)
        self.direction[1] = math.sin(self.angle)

        self.angle %= 2 * math.pi

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
        self.draw_ray_casting(50)
        self.draw_ray(self.angle)

    def draw_ray(self,angle,color=(255,0,0)):
        start_x,start_y = self.rect.center
        end_x,end_y = start_x + 500*math.cos(angle),start_y + 500*math.sin(angle)
        pygame.draw.line(self.game.screen,color,(start_x,start_y),(end_x,end_y))

    def draw_ray_casting(self, fov):
        steps = 50
        fov = math.radians(fov)
        angular_shift = fov / steps
        start_angle = self.angle - fov/2
        for step in range(steps):
            self.draw_ray(start_angle + step*angular_shift,(0,255,0))








