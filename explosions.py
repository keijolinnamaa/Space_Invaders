from pygame.sprite import Sprite
import pygame

class Explosions(Sprite):
    """Explosion class"""
    def __init__(self, center, obj, game):
        super().__init__()
        self.obj = obj
        self.image = game.explosion_anim[self.obj][0] # set first 'alien' image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 #ms
        self.game = game

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate: #if 50ms has passed
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.explosion_anim[self.obj]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.explosion_anim[self.obj][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

    