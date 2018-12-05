import random
import pygame
from AI import AI


class AkhiAI(AI):
    BOX_HEIGHT = 200
    BOX_WIDTH = 200

    def get_velocity(self, list_bullets, pos):
        if not list_bullets:
            return 0, 0
        
        box_left = pos[0] - AkhiAI.BOX_WIDTH
        box_right = pos[0] + AkhiAI.BOX_WIDTH
        box_up = pos[1] + AkhiAI.BOX_HEIGHT
        box_down = pos[1] - AkhiAI.BOX_HEIGHT

        x_sum = 0
        y_sum = 0
        for bullet in list_bullets:
            #if bullet.x > box_left and bullet.x < box_right and bullet.y < box_up and bullet.y > box_down:
            x_sum += bullet.x
            y_sum += bullet.y

        average_x = x_sum // len(list_bullets)
        average_y = y_sum // len(list_bullets)

        return pos[0] - average_x, pos[1] - average_y
