import pygame.font
from pygame.sprite import Group
from ship import Ship


class ScoreBoard:
    """Score board class"""
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.game = game

        self.text_color = (128,128,128)
        self.font = pygame.font.SysFont(None, 48)

        self.prepare_score()
        self.prepare_highscore()
        self.prepare_ships()
        self.prepare_level()

    def prepare_score(self):
        rouded_score = round(self.stats.score, -1)
        score_str = "Score  "+"{:,}".format(rouded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right -20
        self.score_rect.top = 20

    def prepare_highscore(self):
        highscore = round(self.stats.highscore, -1)
        highscore_str = "High Score  "+"{:,}".format(highscore)
        self.highscore_image = self.font.render(highscore_str, True, self.text_color)
        self.highscore_rect = self.highscore_image.get_rect()
        self.highscore_rect.centerx = self.screen_rect.centerx
        self.highscore_rect.top = self.score_rect.top

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highscore_image, self.highscore_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_highscore(self):
        if self.stats.score > self.stats.highscore:
            self.stats.highscore = self.stats.score
            self.prepare_highscore()
            with open ("highscore.txt", "w") as f:
                f.write(str(self.stats.highscore))

    def prepare_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prepare_level(self):
        level_str = "Lvl  "+str(self.stats.level)
        self.level_image =self.font.render(level_str, True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


