import pygame
import time
from math import inf, sqrt, isnan
import random
from pybullethell.AI import AI

SHOW_VISUALS = False


class Line(object):
    THRESHOLD = 60

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        if x1 == x2:
            self.gradient = inf
        else:
            self.gradient = (y1 - y2) / (x1 - x2)
        self.y_intercept = y1 - (self.gradient * x1)

    def is_on_line(self, x, y):
        calc_value = (x * self.gradient) + self.y_intercept - y
        if isnan(calc_value):
            calc_value = self.x2 - x
        return Line.THRESHOLD * -1 <= calc_value <= Line.THRESHOLD

    def get_y_for_x(self, x):
        return (x * self.gradient) + self.y_intercept


class AkhiAI(AI):
    BOX_WIDTH = 200
    BOX_HEIGHT = 250
    SLOW_FACTOR = 1
    LOOKAHEAD_FACTOR = 10
    TIMEOUT = 2

    def __init__(self, width, height, player_size, player_speed):
        self.width = width
        self.height = height
        self.player_size = player_size
        self.player_speed = player_speed
        self.caught_bullets = {}
        self.list_of_lines = {}
        self.fully_caught_bullets = set()
        self.slow_counter = 0

    def get_velocity(self, list_bullets, pos):
        obsolete_lines = set()
        for line in self.list_of_lines.keys():
            if self.list_of_lines[line] not in list_bullets:
                obsolete_lines.add(line)
        for line in obsolete_lines:
            if line in self.list_of_lines.keys():
                del self.list_of_lines[line]

        box_left = pos[0] - AkhiAI.BOX_WIDTH
        box_right = pos[0] + AkhiAI.BOX_WIDTH + self.player_size
        box_up = pos[1] + AkhiAI.BOX_HEIGHT
        box_down = pos[1] - AkhiAI.BOX_HEIGHT + self.player_size

        if SHOW_VISUALS:
            pygame.draw.polygon(AI.SURFACE, pygame.Color('orange'), [(box_left, box_up),
                                                                 (box_right, box_up),
                                                                 (box_right, box_down),
                                                                 (box_left, box_down)], 2)

            for line in self.list_of_lines.keys():
                for x in range(self.width):
                    y = line.get_y_for_x(x)
                    if isnan(y):
                        AI.SURFACE.set_at((round(line.x2), x), (0, 0, 252, 0))
                    else:
                        AI.SURFACE.set_at((x, round(y)), (0, 0, 252, 0))

        for bullet in self.caught_bullets.keys():
            if box_left + bullet.SIZE + 1 < bullet.x < box_right - bullet.SIZE - 1 \
                    and box_down + bullet.SIZE + 1 < bullet.y < box_up - bullet.SIZE - 1 \
                    and bullet not in self.fully_caught_bullets:
                self.list_of_lines[(Line(self.caught_bullets[bullet][0] + bullet.SIZE / 2,
                                         self.caught_bullets[bullet][1] + bullet.SIZE / 2,
                                         bullet.x + bullet.SIZE / 2,
                                         bullet.y + bullet.SIZE / 2))] = bullet
                self.fully_caught_bullets.add(bullet)

        for bullet in list_bullets:
            if box_left < bullet.x < box_right and box_down < bullet.y < box_up:
                self.caught_bullets[bullet] = bullet.x, bullet.y

        minimum_bullet = None
        minimum_distance = inf
        player_center_x = pos[0] + (self.player_size / 2)
        player_center_y = pos[1] + (self.player_size / 2)
        for line in self.list_of_lines.keys():
            if line.is_on_line(player_center_x, player_center_y):
                for bullet in self.fully_caught_bullets:
                    distance = sqrt((bullet.x - player_center_x) ** 2 + (bullet.y - player_center_y) ** 2)
                    if distance < minimum_distance:
                        minimum_distance = distance
                        minimum_bullet = bullet

        self.slow_counter = (self.slow_counter + 1) % AkhiAI.SLOW_FACTOR
        if minimum_bullet and (self.slow_counter == 1 or AkhiAI.SLOW_FACTOR == 1):
            bullet_center_x = (minimum_bullet.x_speed * AkhiAI.LOOKAHEAD_FACTOR) + minimum_bullet.x + bullet.SIZE / 2
            bullet_center_y = (minimum_bullet.y_speed * AkhiAI.LOOKAHEAD_FACTOR) + minimum_bullet.y + bullet.SIZE / 2
            if SHOW_VISUALS:
                pygame.draw.line(AI.SURFACE, pygame.Color('red'),
                                 (player_center_x, player_center_y),
                                 (bullet_center_x, bullet_center_y), 2)
            return_x, return_y = (bullet_center_x - player_center_x) * -1, (bullet_center_y - player_center_y) * -1
        else:
            return_x, return_y = 0, 0

        if not list_bullets:
            return 0, 0

        if not return_x == 0:
            return_x = (int(return_x / abs(return_x)))
        if not return_y == 0:
            return_y = (int(return_y / abs(return_y)))

        timeout = time.time() + AkhiAI.TIMEOUT
        while time.time() < timeout:
            will_collide = True
            for bullet in list_bullets:
                next_bullet_x = bullet.x + bullet.x_speed + bullet.SIZE / 2
                next_bullet_y = bullet.y + bullet.y_speed + bullet.SIZE / 2
                next_player_x = pos[0] + (self.player_size / 2) + (return_x * self.player_speed)
                next_player_y = pos[1] + (self.player_size / 2) + (return_y * self.player_speed)

                top_left_bullet = next_bullet_x - bullet.SIZE / 2, next_bullet_y - bullet.SIZE / 2
                bottom_right_bullet = next_bullet_x + bullet.SIZE / 2, next_bullet_y + bullet.SIZE / 2
                top_left_player = next_player_x - self.player_size / 2, next_player_y - self.player_size / 2
                bottom_right_player = next_player_x + self.player_size / 2, next_player_y + self.player_size / 2

                if top_left_bullet[0] < bottom_right_player[0]\
                   and bottom_right_bullet[0] > top_left_player[0]\
                   and top_left_bullet[1] < bottom_right_player[1]\
                   and bottom_right_bullet[1] > top_left_player[1]:
                    will_collide = True
                    break

                will_collide = False

            if not will_collide:
                break
            else:
                if SHOW_VISUALS:
                    pygame.draw.line(AI.SURFACE, pygame.Color('purple'),
                                 (player_center_x, player_center_y),
                                 (bullet.x + bullet.x_speed * 100 + bullet.SIZE / 2, bullet.y + bullet.y_speed * 100 + bullet.SIZE / 2), 2)
                return_x, return_y = random.choice([(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)])

        return return_x, return_y
