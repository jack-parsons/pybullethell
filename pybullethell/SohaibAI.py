import pygame
import random
from AI import AI


class Line(object):
    THRESHOLD = 100
    
    def __init__(self, x1, y1, x2, y2, x_speed, y_speed):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x_speed = x_speed
        self.y_speed = y_speed
        
        if x1 == x2:
            self.gradient = 0
        else:
            self.gradient = (y1 - y2) / (x1 - x2)
        self.y_intercept = y1 - (self.gradient * x1)

    def is_on_line(self, x, y):
        calc_y = self.get_y_for_x(x)
        return Line.THRESHOLD <= calc_y <= Line.THRESHOLD

    def get_y_for_x(self, x):
        return (x * self.gradient) + self.y_intercept


class SohaibAI(AI):
    BOX_WIDTH = 100
    BOX_HEIGHT = 120

    def __init__(self, width, height, player_size, player_speed):
        self.width = width
        self.height = height
        self.player_size = player_size
        self.player_speed = player_speed
        self.caught_bullets = {}
        self.set_of_lines = set()
        self.fully_caught_bullets = set()

    def get_velocity(self, list_bullets, pos):
        box_left = pos[0] - SohaibAI.BOX_WIDTH
        box_right = pos[0] + SohaibAI.BOX_WIDTH + self.player_size
        box_up = pos[1] + SohaibAI.BOX_HEIGHT
        box_down = pos[1] - SohaibAI.BOX_HEIGHT + self.player_size

        pygame.draw.polygon(AI.SURFACE, pygame.Color('red'), [(box_left, box_up),
                                                              (box_right, box_up),
                                                              (box_right, box_down),
                                                              (box_left, box_down)], 2)

        pygame.draw.line(AI.SURFACE, )
        
        for bullet in list_bullets:
            if box_left < bullet.x < box_right and box_down < bullet.y < box_up:
                self.caught_bullets[bullet] = bullet.x, bullet.y
                
        for bullet in self.caught_bullets.keys():
            if bullet.x > box_left + bullet.SIZE + 1 and bullet.x < box_right - bullet.SIZE - 1 and bullet.y < box_up - bullet.SIZE - 1 and bullet.y > box_down + bullet.SIZE + 1 and bullet not in self.fully_caught_bullets:
                self.set_of_lines.add(Line(self.caught_bullets[bullet][0], self.caught_bullets[bullet][1], bullet.x, bullet.y, bullet.x_speed, bullet.y_speed))
                self.fully_caught_bullets.add(bullet)

        for line in self.set_of_lines:
            print("TEST")
            if line.is_on_line(pos[0], pos[1]):
                return line.x_speed * -1, line.y_speed * -1
            else:
                return 0, 0

        return 0, 0
