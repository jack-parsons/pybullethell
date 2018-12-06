import pygame
from AI import AI


class Human(AI):
    BOX_HEIGHT = 500
    BOX_WIDTH = 600

    def get_velocity(self, list_bullets, pos):
        x = 0
        y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y = 1

        return x, y