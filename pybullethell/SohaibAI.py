import pygame
from math import inf, sqrt
import random
from AI import AI


class Line(object):
    THRESHOLD = 52
    
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        if x1 == x2:
            self.gradient = 0
        else:
            self.gradient = (y1 - y2) / (x1 - x2)
        self.y_intercept = y1 - (self.gradient * x1)

    def is_on_line(self, x, y):
        calc_value = (x * self.gradient) + self.y_intercept - y
        return Line.THRESHOLD * -1 <= calc_value <= Line.THRESHOLD

    def get_y_for_x(self, x):
        return (x * self.gradient) + self.y_intercept


class SohaibAI(AI):
    BOX_WIDTH = 200
    BOX_HEIGHT = 250

    def __init__(self, width, height, player_size, player_speed):
        self.width = width
        self.height = height
        self.player_size = player_size
        self.player_speed = player_speed
        self.caught_bullets = {}
        self.list_of_lines = []
        self.fully_caught_bullets = set()

    def get_velocity(self, list_bullets, pos):

        """
        if self.list_of_lines and list_bullets:
            for _ in range(len(self.list_of_lines) - len(list_bullets)):
        """


        box_left = pos[0] - SohaibAI.BOX_WIDTH
        box_right = pos[0] + SohaibAI.BOX_WIDTH + self.player_size
        box_up = pos[1] + SohaibAI.BOX_HEIGHT
        box_down = pos[1] - SohaibAI.BOX_HEIGHT + self.player_size

        # for line in self.list_of_lines:
            # for x in range(self.width):
             #    AI.SURFACE.set_at((x, round(line.get_y_for_x(x))), (0,255,152,0))

        for bullet in self.caught_bullets.keys():
            if box_left + bullet.SIZE + 1 < bullet.x < box_right - bullet.SIZE - 1\
                    and box_down + bullet.SIZE + 1 < bullet.y < box_up - bullet.SIZE - 1\
                    and bullet not in self.fully_caught_bullets:
                self.list_of_lines.append(Line(self.caught_bullets[bullet][0] + bullet.SIZE / 2,
                                               self.caught_bullets[bullet][1] + bullet.SIZE / 2,
                                               bullet.x + bullet.SIZE / 2,
                                               bullet.y + bullet.SIZE / 2))
                self.fully_caught_bullets.add(bullet)

        for bullet in list_bullets:
            if box_left < bullet.x < box_right and box_down < bullet.y < box_up:
                self.caught_bullets[bullet] = bullet.x, bullet.y

        minimum_bullet = None
        minimum_distance = inf
        player_center_x = pos[0] + (self.player_size / 2)
        player_center_y = pos[1] + (self.player_size / 2)
        for line in self.list_of_lines:
            if line.is_on_line(pos[0], pos[1]):
                for bullet in self.fully_caught_bullets:
                    distance = sqrt((bullet.x - player_center_x) ** 2 + (bullet.y - player_center_y) ** 2)
                    if distance < minimum_distance:
                        minimum_distance = distance
                        minimum_bullet = bullet

        if minimum_bullet:
            bullet_center_x = minimum_bullet.x + bullet.SIZE / 2
            bullet_center_y = minimum_bullet.y + bullet.SIZE / 2
            pygame.draw.line(AI.SURFACE, pygame.Color('red'),
                             (player_center_x, player_center_y),
                             (bullet_center_x, bullet_center_y), 2)
            return (bullet_center_x - player_center_x) * -1, (bullet_center_y - player_center_y) * -1
        else:
            return 0, 0