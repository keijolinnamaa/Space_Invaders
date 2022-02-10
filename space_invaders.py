import sys
import os.path
from datetime import datetime
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from explosions import Explosions
from scoreboard import ScoreBoard
import random

class SpaceInvaders:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()        
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.bg_image = pygame.image.load("images/starfield.png").convert_alpha()
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        self.bg_color = (self.settings.bg_color)
        pygame.display.set_caption("Space Invaders")
        self.play_button = Button(self, "Play")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()        
        self.stats = GameStats(self)
        self.stats.highscore = self.get_highscore()
        self.sb = ScoreBoard(self)
        #self.sound_dir = os.path.join(os.path.dirname((__file__), "sounds")

        
        
        self.create_fleet()
        self.setup_explosions()
        self.setup_sounds()


        
    def run_game(self):
        """Main loop"""
        pygame.mixer.music.play(loops= -1)
        while True:            
            self.check_events()
            if self.stats.game_active:
                self.explosions.update()
                self.ship.update()
                self.update_bullets()
                self.update_aliens()                       
            self.update_screen()   

    def get_highscore(self):        
            try:
                with open ("highscore.txt", "r") as f:
                    highscore = f.readline().strip()  
                    if highscore == "":
                        highscore = 0
                    return int(highscore) 
            except:
                with open ("highscore.txt", "w") as f:
                    f.write("0")
                return 0 
            
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def _check_keydown_events(self, event): 
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        

    def _check_keyup_events(self, event):        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def setup_sounds(self):
        #background
        pygame.mixer.music.load("sounds/alex.mp3")
        pygame.mixer.music.set_volume(0.5)
        #effects
        self.shooting_sounds = []
        sound_dir = os.path.join(os.path.dirname(__file__), "sounds")
        for sound in ['laser.wav', 'laser2.wav']:
            self.shooting_sounds.append(pygame.mixer.Sound(os.path.join(sound_dir, sound)))

        for s in self.shooting_sounds:
            s.set_volume(0.5)

        self.explosion_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'explosion.wav'))
        self.explosion_sound.set_volume(0.5)


    def check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.setup_dynamic_settings()
            self.sb.prepare_score()
            self.sb.prepare_level()
            self.sb.prepare_ships()
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            self.stats.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self.create_fleet()
            self.ship.center_ship()

    def setup_explosions(self):
        self.explosion_anim = {}
        self.explosion_anim['alien'] = []
        self.explosion_anim['ship'] = []
        #and also we could make eg. self.explosion_anim['ship'] = []
        for i in range(9): #0-8
            filename = f'regularExplosion0{i}.png'
            img = pygame.image.load("images/"+filename).convert_alpha()
            #alien explosion
            img_alien = pygame.transform.scale(img, (70,70))
            self.explosion_anim['alien'].append(img_alien)
            #ship explosion
            img_ship = pygame.transform.scale(img, (140,140))
            self.explosion_anim['ship'].append(img_ship)

    def check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            pygame.mixer.Sound.play(self.explosion_sound)
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points *len(aliens)        
                for alien in aliens:
                    explosion = Explosions(alien.rect.center, 'alien', self)
                    self.explosions.add(explosion)
            self.sb.prepare_score()
            self.sb.check_highscore()
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prepare_level()

    

    def fire_bullet(self):        
        '''Creates new bullet instance and adds it to the bullets sprite group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            pygame.mixer.Sound.play(self.shooting_sounds[0])
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_of_aliens_x = available_space_x // (2*alien_width)
        available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)
        number_of_aliens_y = available_space_y // (2*alien_height)
        for row in range(number_of_aliens_y):
            for alien_number in range(number_of_aliens_x):
                self.create_alien(alien_number, row)

    def create_alien(self, alien_number, row):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2*alien_width*alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien_height + (2*alien_height*row)
        self.aliens.add(alien)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def ship_hit(self):
        explosion = Explosions(self.ship.rect.center, 'ship', self)
        self.explosions.add(explosion)
        pygame.mixer.Sound.play(self.explosion_sound)
        for i in range(500):
            self.explosions.update()                           
            self.update_screen()   
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.prepare_ships()
            self.aliens.empty()
            self.bullets.empty()
            self.create_fleet()
            self.ship.center_ship()
            
        else:
            self.stats.game_active = False
            self.stats.reset_stats()
            pygame.mouse.set_visible(True)

    def check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()                
                break

    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()        
        if pygame.sprite.spritecollideany(self.ship,self.aliens):            
            self.ship_hit()            
        self.check_aliens_bottom()

    def update_bullets(self):
        self.bullets.update()
        # Get rid of bullets that have disappeared from the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self.check_bullet_alien_collisions()

    def update_screen(self):
        #self.screen.fill(self.bg_color)
        self.screen.blit(self.bg_image, self.screen.get_rect()) #backgroundimage
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #make the most recent drawn screen visible
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.screen.fill(self.bg_color)
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == "__main__":
    si = SpaceInvaders()
    si.run_game()
