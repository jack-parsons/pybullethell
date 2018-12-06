import pygame
from random import choice
from pybullethell.AI import AI


class PredictAI(AI):
    BOX_HEIGHT = 500
    BOX_WIDTH = 600
    POSITIONS = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]

    def get_velocity(self, list_bullets, pos):
        if not list_bullets:
            return 0, 0

        while True:
            will_collide = True
            randpos = choice(PredictAI.POSITIONS)
            for bullet in list_bullets:
                next_bullet_x = bullet.x + bullet.x_speed + bullet.SIZE / 2
                next_bullet_y = bullet.y + bullet.y_speed + bullet.SIZE / 2
                next_player_x = pos[0] + (self.player_size / 2) + (randpos[0] * self.player_speed)
                next_player_y = pos[1] + (self.player_size / 2) + (randpos[1] * self.player_speed)

                top_left_bullet = next_bullet_x - bullet.SIZE / 2, next_bullet_y - bullet.SIZE / 2
                bottom_right_bullet = next_bullet_x + bullet.SIZE / 2, next_bullet_y + bullet.SIZE / 2
                top_left_player = next_player_x - self.player_size / 2, next_player_y - self.player_size / 2
                bottom_right_player = next_player_x + self.player_size / 2, next_player_y + self.player_size / 2

                pygame.draw.polygon(AI.SURFACE, pygame.Color("green"), [top_left_bullet, (top_left_bullet[0] + bullet.SIZE, top_left_bullet[1]), bottom_right_bullet, (bottom_right_bullet[0] - bullet.SIZE, bottom_right_bullet[1])], 2)
                pygame.draw.polygon(AI.SURFACE, pygame.Color("red"),
                                    [top_left_player, (top_left_player[0] + self.player_size, top_left_player[1]),
                                     bottom_right_player,
                                     (bottom_right_player[0] - self.player_size, bottom_right_player[1])], 2)
                if top_left_bullet[0] > bottom_right_player[0] or top_left_player[0] > bottom_right_bullet[0]:
                    will_collide = False
                    continue
                if top_left_bullet[1] < bottom_right_player[1] or top_left_player[1] < bottom_right_bullet[1]:
                    will_collide = False
                    continue

                print("TEST")
                will_collide = True
                break

            if not will_collide:
                break

        return randpos
