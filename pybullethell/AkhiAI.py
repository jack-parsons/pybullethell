import random
import pygame
from math import sqrt, inf
from AI import AI


class AkhiAI(AI):
    BOX_HEIGHT = 500
    BOX_WIDTH = 600

    def get_velocity(self, list_bullets, pos):
        if pos[0] < self.width / 4:
            return 1, 0
        if pos[0] > self.width * (3/4):
            return -1, 0
        if pos[1] < self.height / 6:
            return 0, 1
        if pos[1] > self.height* (5/6):
            return 0, -1

        if not list_bullets:
            return 0, 0
        
        box_left = pos[0] - AkhiAI.BOX_WIDTH
        box_right = pos[0] + AkhiAI.BOX_WIDTH
        box_up = pos[1] + AkhiAI.BOX_HEIGHT
        box_down = pos[1] - AkhiAI.BOX_HEIGHT

        minimum_bullet = None
        minimum_distance = inf
        for bullet in list_bullets:
            if bullet.x > box_left and bullet.x < box_right and bullet.y < box_up and bullet.y > box_down:
                distance = sqrt((bullet.x - pos[0]) ** 2 + (bullet.y - pos[1]) ** 2)
                if distance < minimum_distance:
                    minimum_distance = distance
                    minimum_bullet = bullet

        pygame.draw.line(AI.SURFACE, pygame.Color('red'), (pos[0], pos[1]), (minimum_bullet.x, minimum_bullet.y), 2)
        return (minimum_bullet.x - pos[0]) * -1, (minimum_bullet.y - pos[1]) * -1
