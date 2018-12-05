from pybullethell.AI import AI
import random


class JackAI(AI):
    def get_velocity(self, list_of_bullets, pos):
        return random.randrange(-1, 2), random.randrange(-1, 2)
