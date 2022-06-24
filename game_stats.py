class GameStats:
    """Game statistics class"""
    def __init__(self,game):
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False #game will start when we press PLAY button.
        self.highscore = 0
        self.score = 0
        

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1