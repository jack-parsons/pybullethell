import random
import pygame
from AI import AI

class RepelAI(AI):
    BOX_HEIGHT = 200
    BOX_WIDTH = 200
    
    def __init__(self, list_bullets):
        self.caught_bullets = []

    def get_velocity(self, list_bullets, pos):
        
        box_left = pos[0] - RepelAI.BOX_WIDTH
        box_right = pos[0] + RepelAI.BOX_WIDTH
        box_up = pos[1] + RepelAI.BOX_HEIGHT
        box_down = pos[1] - RepelAI.BOX_HEIGHT
        
        in_box = False
        for bullet in list_bullets:
            if bullet.x > box_left and bullet.x < box_right and bullet.y < box_up and bullet.y > box_down:
                if bullet not in self.caught_bullets:
                    bullet.x_speed *= -1
                    bullet.y_speed *= -1
                    self.caught_bullets.append(bullet)
                    continue

        return random.choice([-1, 1]), random.choice([-1, 1])
