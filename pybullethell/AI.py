class AI:
    def __init__(self, width, height, player_size, player_speed):
        self.width = width
        self.height = height
        self.player_size = player_size
        self.player_speed = player_speed

    # list_bullets is a list of positions of bullets
    # pos is a tuple (x, y) for the player
    def get_velocity(self, list_bullets, pos):
       return 0, 0  # return tuple for coordinates
