

import pygame
from pygame.sprite import Sprite
from random import randint

class Alien(Sprite):

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.image = pygame.image.load("images/onyx.png").convert_alpha()       #("images/ship.bmp").convert()
        #self.image.set_colorkey((230,230,230))
        #self.image.set_alpha(randint(70,127))

        self.setings = game.settings

        self.rect = self.image.get_rect()
        self.rect.x =self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += self.setings.alien_speed * self.setings.fleet_direction
        self.rect.x = self.x

