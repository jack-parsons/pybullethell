from pybullethell.AI import AI
import random
from math import *
import pygame


class Vector:
    def __init__(self, x, y, cartesian=True):
        self.x = x
        self.y = y
        self.mag = x
        self.dir = y
        if cartesian:
            self.mag = self.get_mag()
            self.dir = self.get_dir()
        else:
            self.x = self.get_x()
            self.y = self.get_y()

    def get_dir(self):
        return atan2(self.y, self.x)

    def get_mag(self):
        return hypot(self.x, self.y)

    def get_x(self):
        return self.mag * cos(self.dir)

    def get_y(self):
        return self.mag * sin(self.dir)

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        return Vector(self.x*other, self.y*other)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise Exception("Not valid index:" + item)

    def normalise(self):
        return Vector(1, self.dir, False)

    def __str__(self):
        return "Vector(%f, %f)" % (self.x, self.y)


class JackAI(AI):

    def get_velocity(self, list_of_bullets, pos):
        velocity = Vector(0, 0)
        pos = Vector(pos[0], pos[1])
        center_pos = Vector(self.width/2, self.height/2)

        for bullet in list_of_bullets:
            bullet_vel = Vector(bullet.x_speed, bullet.y_speed)
            perp_dist = -(pos.mag - Vector(bullet.x_speed, bullet.y_speed).mag) * tan(velocity.dir - bullet_vel.dir)
            if (pos - Vector(bullet.x, bullet.y)).mag < self.player_size * 3:
                velocity += (pos - Vector(bullet.x, bullet.y)).normalise() * (1/(pos - Vector(bullet.x, bullet.y)).mag)**2
        if velocity.mag != 0:
            return velocity.normalise()
        elif (center_pos - pos).mag > self.player_speed:
            return (center_pos - pos).normalise()
        else:
            return Vector(0, 0)


    # def get_velocity(self, list_of_bullets, pos):
    #     if len(list_of_bullets) > 0:
    #         min_dist_bullet = list_of_bullets[0]
    #         min_dist = hypot(min_dist_bullet.x-pos[0], min_dist_bullet.y-pos[1])
    #         for bullet in list_of_bullets:
    #             dist = hypot(bullet.x-pos[0], bullet.y-pos[1])
    #             if min_dist > dist:
    #                 min_dist = dist
    #                 min_dist_bullet = bullet
    #         if min_dist < self.player_speed * 10:
    #             return -(min_dist_bullet.x-pos[0]), -(min_dist_bullet.y-pos[1])
    #         if min_dist > self.player_speed * 30:
    #             return 0, 0
    #         if pos[0] < min_dist:
    #             return 1, 0
    #         elif self.width - pos[0] < min_dist:
    #             return -1, 0
    #         elif pos[1] < min_dist:
    #             return 0, 1
    #         elif self.height - pos[1] < min_dist:
    #             return 0, -1
    #         else:
    #             return -(min_dist_bullet.x-pos[0]), -(min_dist_bullet.y-pos[1])
    #     return 0, 0

    # def get_velocity(self, list_of_bullets, pos):

