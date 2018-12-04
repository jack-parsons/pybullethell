import random
import pygame
from AI import AI

class SohaibAI(AI):
    BOX_HEIGHT = 200
    BOX_WIDTH = 200
    
    def __init__(self, list_bullets):
        self.caught_bullets = {}

    def get_velocity(self, list_bullets, pos):
        
        box_left = pos[0] - AkhiAI.BOX_WIDTH
        box_right = pos[0] + AkhiAI.BOX_WIDTH
        box_up = pos[1] + AkhiAI.BOX_HEIGHT
        box_down = pos[1] - AkhiAI.BOX_HEIGHT
        
        in_box = False
        for bullet in list_bullets:
            if bullet.x > box_left and bullet.x < box_right and bullet.y < box_up and bullet.y > box_down:
                self.caught_bullets[bullet] = bullet.x, bullet.y
                
        for bullet in caught_bullets.keys():
            if bullet.x > box_left + bullet.size and bullet.x < box_right - bullet.size and bullet.y < box_up - bullet.size and bullet.y > box_down + bullet.size:
