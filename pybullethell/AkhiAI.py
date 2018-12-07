import random
import pygame
from math import sqrt, inf
from pybullethell.AI import AI


class AkhiAI(AI):
    BOX_HEIGHT = 150
    BOX_WIDTH = 175
    SLOW_FACTOR = 3
    LOOKAHEAD_FACTOR = 10

    def __init__(self, width, height, player_size, player_speed):
        self.width = width
        self.height = height
        self.player_size = player_size
        self.player_speed = player_speed
        self.slow_counter = 0

    def get_velocity(self, list_bullets, pos):
        if pos[0] < self.width / 4:
            return 1, 0
        if pos[0] > self.width * (3/4):
            return -1, 0

        box_left = pos[0] - AkhiAI.BOX_WIDTH
        box_right = pos[0] + AkhiAI.BOX_WIDTH + self.player_size
        box_up = pos[1] + AkhiAI.BOX_HEIGHT
        box_down = pos[1] - AkhiAI.BOX_HEIGHT + self.player_size

        player_center_x = pos[0] + (self.player_size / 2)
        player_center_y = pos[1] + (self.player_size / 2)
        minimum_bullet = None
        minimum_distance = inf
        for bullet in list_bullets:
            if box_left < bullet.x < box_right and box_down < bullet.y < box_up:
                distance = sqrt((bullet.x - player_center_x) ** 2 + (bullet.y - player_center_y) ** 2)
                if distance < minimum_distance:
                    minimum_distance = distance
                    minimum_bullet = bullet

        if not list_bullets or not minimum_bullet:
            return 0, 0

        self.slow_counter = (self.slow_counter + 1) % AkhiAI.SLOW_FACTOR
        if self.slow_counter == 1:
            bullet_center_x = (minimum_bullet.x_speed * AkhiAI.LOOKAHEAD_FACTOR) + minimum_bullet.x + bullet.SIZE / 2
            bullet_center_y = (minimum_bullet.y_speed * AkhiAI.LOOKAHEAD_FACTOR) + minimum_bullet.y + bullet.SIZE / 2
            pygame.draw.line(AI.SURFACE, pygame.Color('red'), (player_center_x, player_center_y), (bullet_center_x, bullet_center_y), 2)
            return (bullet_center_x - player_center_x) * -1, (bullet_center_y - player_center_y) * -1
        else:
            return 0, 0