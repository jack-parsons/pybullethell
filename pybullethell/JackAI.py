from pybullethell.AI import AI
import random
from math import *


class JackAI(AI):
    def get_velocity(self, list_of_bullets, pos):
        if len(list_of_bullets) > 0:
            min_dist_bullet = list_of_bullets[0]
            min_dist = hypot(min_dist_bullet.x-pos[0], min_dist_bullet.y-pos[1])
            for bullet in list_of_bullets:
                dist = hypot(bullet.x-pos[0], bullet.y-pos[1])
                if min_dist > dist:
                    min_dist = dist
                    min_dist_bullet = bullet
            if min_dist < self.player_speed * 10:
                return -(min_dist_bullet.x-pos[0]), -(min_dist_bullet.y-pos[1])
            if min_dist > self.player_speed * 30:
                return 0, 0
            if pos[0] < min_dist:
                return 1, 0
            elif self.width - pos[0] < min_dist:
                return -1, 0
            elif pos[1] < min_dist:
                return 0, 1
            elif self.height - pos[1] < min_dist:
                return 0, -1
            else:
                return -(min_dist_bullet.x-pos[0]), -(min_dist_bullet.y-pos[1])

        return 0, 0
