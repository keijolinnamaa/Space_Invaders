import pygame
#import os.path

#img_dir = os.path.join(os.path.dirname(__file__), "images")


class Settings:
    def __init__(self):
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)
        #self.bg_image = pygame.image.load("images/starfield.png").convert_alpha()
        #self.bg_image = pygame.image.load(os.path.(img_dir, "starfield.png")).convert_alpha()
        self.ship_limit = 3
        #Bullet settings
        
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (247,14,240)
        self.bullets_allowed = 3

        #Alien settings
        self.fleet_drop_speed = 10

        #Difficulty set
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.setup_dynamic_settings()

        #Text for gametext info
        self.font = pygame.font.SysFont(None, 48)


    def setup_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.alien_speed = 1.0
        self.alien_points = 10
        self.fleet_direction = 1


    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)