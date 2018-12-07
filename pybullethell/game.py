import pygame
import random
from itertools import permutations
from objects import Player, Bullet
from pybullethell.AkhiAI import *
from pybullethell.SohaibAI import *
from pybullethell.Human import *
from pybullethell.PredictAI import *
from pybullethell.JackAI import JackAI


class Game:
    def __init__(self, size_x, size_y, ticks_per_bullet=10):
        self.size_x = int(size_x)
        self.size_y = int(size_y)
        self.field = pygame.Rect(0, 0, size_x, size_y)
        self.bullets = []
        self.players = [
            Player(self.size_x*(0.25+random.random()*0.5), self.size_y*(0.25+random.random()*0.5), self.size_x, self.size_y, self.bullets, SohaibAI(self.size_x, self.size_y, Player.SIZE, Player.SPEED)),
            Player(self.size_x * (0.25 + random.random() * 0.5), self.size_y * (0.25 + random.random() * 0.5), self.size_x, self.size_y, self.bullets, JackAI(self.size_x, self.size_y, Player.SIZE, Player.SPEED)),
            Player(self.size_x*(0.25+random.random()*0.5), self.size_y*(0.25+random.random()*0.5), self.size_x, self.size_y, self.bullets, AkhiAI(self.size_x, self.size_y, Player.SIZE, Player.SPEED))
        ]
        
        self.font = pygame.font.Font(None, 30)
        self.score = 0
        self.ticks_per_bullet = ticks_per_bullet
        self.a_player_alive = True

    def tick(self):
        for player in self.players:
            player.tick(self.bullets)
        for bullet in self.bullets:
            bullet.tick()

        bullet_hitboxes = [b.hitbox() for b in self.bullets]

        self.bullets = [self.bullets[i] for i
                        in self.field.collidelistall(bullet_hitboxes)]
        for player in self.players:
            if (player.alive and
                    player.hitbox().collidelist(bullet_hitboxes) != -1):
                player.alive = False
                self.bullets += Game.death_explosion(player.x, player.y)
            if not player.alive:
                self.a_player_alive = False

        if self.a_player_alive:
            self.score += 1

        if self.a_player_alive and not random.randrange(self.ticks_per_bullet):
            self.bullets.append(self.random_bullet())

    def draw(self, surface):
        for player in self.players:
            player.draw(surface)
            for bullet in self.bullets:
                bullet.draw(surface)
            self.draw_score(surface)
            if not player.alive:
                self.draw_newgame_message(surface)

    def random_bullet(self):
        max_speed = 3
        speed_x, speed_y = 0, 0
        while speed_x == 0 and speed_y == 0:
            speed_x = random.randrange(-max_speed, max_speed)
            speed_y = random.randrange(-max_speed, max_speed)
        axis = random.choice('xy')
        if axis == 'x':
            position_x = random.randrange(self.size_x)
            position_y = 0 if speed_y > 0 else self.size_y
        else:
            position_y = random.randrange(self.size_y)
            position_x = 0 if speed_x > 0 else self.size_x
        return Bullet(position_x, position_y, speed_x, speed_y)

    def draw_score(self, surface):
        rendered_text = self.font.render('{}'.format(self.score), True,
                                         pygame.Color('white'))
        surface.blit(rendered_text, (10, 10))

    def draw_newgame_message(self, surface):
        rendered_text = self.font.render('Press SPACE for new game', True,
                                         pygame.Color('white'))
        surface.blit(rendered_text,
                     (10, self.size_y - rendered_text.get_height() - 10))

    def death_explosion(x, y):
        return list([Bullet(x, y, xs, ys, pygame.Color('white')) for xs, ys
                     in permutations(list(range(-10, 10)), 2)
                     if (xs, ys) != (0, 0)])
