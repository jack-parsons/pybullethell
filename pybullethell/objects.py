from abc import ABC, abstractmethod
import pygame


class GameObject(ABC):

    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def hitbox(self):
        pass

    @abstractmethod
    def tick(self, list_of_bullets):
        pass


class Player(GameObject):
    SPEED = 5
    SIZE = 30

    def __init__(self, x, y, game_size_x, game_size_y, bullet_list, ai):
        self.x = x
        self.y = y
        self.game_size_x = game_size_x
        self.game_size_y = game_size_y
        self.alive = True
        self.ai = ai

    def hitbox(self):
        return pygame.Rect(self.x, self.y, Player.SIZE, Player.SIZE)

    def tick(self, list_of_bullets):
        position = self.ai.get_velocity(list_of_bullets, (self.x, self.y))

        if self.x < 0:
            self.x = 0
            return
        if self.x > self.game_size_x - Player.SIZE:
            self.x = self.game_size_x - Player.SIZE
            return
        if self.y < 0:
            self.y = 0
            return
        if self.y > self.game_size_y - Player.SIZE:
            self.y = self.game_size_y - Player.SIZE
            return

        if not position[0] == 0:
            self.x += (int(position[0] / abs(position[0]))) * Player.SPEED

        if not position[1] == 0:
            self.y += (int(position[1] / abs(position[1]))) * Player.SPEED

    def draw(self, surface):
        if self.alive:
            color = (pygame.Color('white') if self.alive
                     else pygame.Color('black'))
            pygame.draw.rect(surface, color,
                             (self.x, self.y, Player.SIZE, Player.SIZE))


class Bullet(GameObject):
    SIZE = 10

    def __init__(self, x, y, x_speed, y_speed, color=pygame.Color('red')):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.color = color

    def hitbox(self):
        return pygame.Rect(self.x, self.y, Bullet.SIZE, Bullet.SIZE)

    def tick(self):
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                         (self.x, self.y, Bullet.SIZE, Bullet.SIZE))


"""

"""    
