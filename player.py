import pygame
import math
import utils

class Player:
    FOV = 60
    NUM_RAYS = 50

    def __init__(self,game):
        self.game = game
        self.rect = pygame.Rect(0,0, self.game.tile_size/4,self.game.tile_size/4)
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
        :param direction:To move forward 1 To move backward -1
        :return: None
        """
        cannot_move_x,cannot_move_y = self.check_collision(direction)
        print(f"Can move in x:{not cannot_move_x}, Can't move in y:{not cannot_move_y}")
        self.rect.x = self.rect.x + direction * self.direction[0] * self.velocity if not cannot_move_x else self.rect.x
        self.rect.y = self.rect.y + direction * self.direction[1] * self.velocity if not cannot_move_y else self.rect.y

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

    def check_collision(self,direction)->tuple[bool,bool]:
        cannot_move_x,cannot_move_y = False,False
        x = self.rect.x
        y = self.rect.y + direction * self.direction[1] * self.velocity

        if self.direction[1]*direction < 0: #We are going up
            top_y = y
            left_x = x
            right_x = x+self.rect.width
            if self.game.is_wall(left_x, top_y) or self.game.is_wall(right_x, top_y):
                cannot_move_y = True
        if self.direction[1]*direction > 0: #We are going down
            bottom_y = y +self.rect.height + 1
            left_x = x
            right_x = x+self.rect.width
            if self.game.is_wall(left_x, bottom_y) or self.game.is_wall(right_x, bottom_y):
                cannot_move_y = True

        x = self.rect.x + direction * self.direction[0] * self.velocity
        y = self.rect.y

        if self.direction[0]*direction < 0: #We are going left
            left_x = x
            top_y = y
            bottom_y = y+self.rect.height
            if self.game.is_wall(left_x,top_y) or self.game.is_wall(left_x,bottom_y):
                cannot_move_x = True
        if self.direction[0]*direction > 0: # We are going right
            right_x = x + self.rect.width + 1
            top_y = y
            bottom_y = y+self.rect.height
            if self.game.is_wall(right_x,top_y) or self.game.is_wall(right_x,bottom_y):
                cannot_move_x = True
        return cannot_move_x,cannot_move_y

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
        self.draw_player()


    def draw_player(self):
        pygame.draw.rect(self.game.screen,(100,100,100),self.rect)
        #pygame.draw.circle(self.game.screen,(100,100,100),self.rect.center,self.rect.width//2)













