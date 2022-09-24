from random import random
from asteroids import Asteroids
import pygame
import random as r
import math
from player import Player
from static import *
# from mode7 import *

def angle(angle):
    new_angle = angle * math.pi / 180
    return new_angle

class Game:
    def __init__(self):
        self.width = 1600
        self.height = 900

        self.level_position = (0,0)

        self.origin = (self.width/2,self.height/2)
        self.game_window = pygame.display.set_mode((self.width,self.height))

        self.clock = pygame.time.Clock()
        self.tick_rate = 60
        self.player = None
        self.num_asteroids = 10
        self.asteroids = [None] * self.num_asteroids             # group of [numAsteroids] (10) asteroids that automatically spawn in
        self.asteroids2 = [None] * 10 * self.num_asteroids       # group of asteroids which can be created from destroyed asteroids
        self.asteroid_spawn_time = 5.0
        self.title_font = None
        self.menu_font = None


        self.selection = 'start'

        self.asteroid_timer = 0
        self.shoot_timer = 0

        # self.Talitor = Mode7("../assets/Talitor.png")
        
        self.hold_up = False
        self.hold_down = False
        self.hold_left = False
        self.hold_right = False
        self.hold_shoot = False

        self.spawn_asteroids()
    
    def drift_asteroids(self, asteroids):
        for i in range(len(asteroids)):
            if asteroids[i] != None:
                asteroids[i].movement_direction = math.atan(-asteroids[i].velocityY/asteroids[i].velocityX) * 180 / math.pi
                # print(self.asteroids[0].movement_direction)

                asteroids[i].rotation += asteroids[i].spin

                # move asteroids based on speed and direction
                asteroids[i].x += asteroids[i].speed * math.cos(angle(asteroids[i].direction))
                asteroids[i].y += asteroids[i].speed * math.sin(angle(asteroids[i].direction))

                # Asteroid level wrap stuff
                if asteroids[i].x > self.width + asteroids[i].avSize:
                    asteroids[i].x = 0 - asteroids[i].avSize
                elif asteroids[i].x < 0 - asteroids[i].avSize:
                    asteroids[i].x = self.width + asteroids[i].avSize
                if asteroids[i].y > self.height + asteroids[i].avSize:
                    asteroids[i].y = 0 - asteroids[i].avSize
                elif asteroids[i].y < 0 - asteroids[i].avSize:
                    asteroids[i].y = self.height + asteroids[i].avSize

    def asteroid_drift(self):
        self.drift_asteroids(self.asteroids)
        self.drift_asteroids(self.asteroids2)
        
    def spawn_asteroids(self):
        for i in range(len(self.asteroids)):
            if self.asteroids[i] == None:
                self.asteroids[i] = Asteroids(self, 3)
                break

    def draw_objects(self):
        self.game_window.fill(colors.get('black'))

        # DRAW STUFF

        # DRAW PLAYER
        if self.player:
            pygame.draw.polygon(self.game_window, colors.get('green'), self.player.generate_points(), 2)

            # DRAW BULLETS
            for i in range(len(self.player.bullets)):
                if self.player.bullets[i] != None:
                    self.player.bullets[i].move(self, self.player)
                    pygame.draw.circle(self.game_window, colors.get('white'),(self.player.bullets[i].x, self.player.bullets[i].y), self.player.bullets[i].size, 0)

        # DRAW ASTEROIDS
        for i in range(len(self.asteroids)):
            if self.asteroids[i] != None:
                pygame.draw.polygon(self.game_window, colors.get('white'), self.asteroids[i].update_points(self), 2)
        for i in range(len(self.asteroids2)):
            if self.asteroids2[i] != None:
                pygame.draw.polygon(self.game_window, colors.get('white'), self.asteroids2[i].update_points(self), 2)
        
        # Update frame
        pygame.display.update()

    def asteroid_timer_func(self):
        if self.asteroid_timer > self.asteroid_spawn_time:
            self.spawn_asteroids()
            self.asteroid_timer = 0

    def shoot_timer_func(self):
        if self.shoot_timer > self.player.shoot_speed:
            self.shoot_timer = 0
        if self.shoot_timer == 0:
            self.player.shoot()
    
    def bullet_timer_func(self):
        if not self.player:
            return
        for i in range(len(self.player.bullets)):
            if self.player.bullets[i] is not None:
                bullet = self.player.bullets[i]
                bullet.bullet_time += (1 / self.tick_rate)
                if bullet.bullet_time > bullet.bullet_time_max:
                    bullet.destroy(self.player, i)

    def check_asteroid_hit_player(self):
        # Big Asteroids
        for asteroid in self.asteroids:
            try:
                if asteroid and self.player:
                    if  abs(asteroid.x - self.player.x) < asteroid.avSize and \
                        abs(asteroid.y - self.player.y) < asteroid.avSize:
                        # Player dies because the distance is smaller than the asteroid size
                        self.kill_player()
            except Exception as e:
                print(e)
        # Small Asteroids
        for asteroid in self.asteroids2:
            try:
                if asteroid and self.player:
                    if  abs(asteroid.x - self.player.x) < asteroid.avSize and \
                        abs(asteroid.y - self.player.y) < asteroid.avSize:
                        # Player dies because the distance is smaller than the asteroid size
                        self.kill_player()
            except Exception as e:
                print(e)

    def kill_player(self):
        self.player = None

    def check_bullet_hit(self):
        if not self.player:
            return
        for i in range(len(self.player.bullets)):
            if self.player.bullets[i] != None:
                bullet = self.player.bullets[i]

                for j in range(len(self.asteroids)):
                    if self.asteroids[j] != None:
                        asteroid = self.asteroids[j]
                        diffX = abs(bullet.x - asteroid.x)
                        diffY = abs(bullet.y - asteroid.y)
                        diff = math.sqrt(diffX**2 + diffY**2)
                        thresh = bullet.size + asteroid.avSize + 4
                        if diff < thresh:
                            asteroid.break_apart(self, self.asteroids, j)
                            bullet.destroy(self.player, i)
                            # print('HIT')
                
                for k in range(len(self.asteroids2)):
                    if self.asteroids2[k] != None:
                        asteroid = self.asteroids2[k]
                        diffX = abs(bullet.x - asteroid.x)
                        diffY = abs(bullet.y - asteroid.y)
                        diff = math.sqrt(diffX**2 + diffY**2)
                        thresh = bullet.size + asteroid.avSize + 2
                        if diff < thresh:
                            asteroid.break_apart(self, self.asteroids2, k)
                            bullet.destroy(self.player, i)
                            # print('HIT')

    def draw_menu(self):
        # Draw background/Window color
        fill_window_color(self, 'black')
        # Set up Title and Menu Text objects
        self.title_font = pygame.font.Font(font_string, title_font_size)
        title_text = self.title_font.render(title_string, False, colors.get('white'))
        self.menu_font = pygame.font.Font(font_string, menu_font_size)
        StartText = self.menu_font.render(StartString, False, colors.get('white'))
        OptionsText = self.menu_font.render(OptionsString, False, colors.get('white'))
        QuitText = self.menu_font.render(QuitString, False, colors.get('white'))

        # Animate asteroids
        for i in range(len(self.asteroids)):
            if self.asteroids[i] != None:
                pygame.draw.polygon(self.game_window, colors.get('white'), self.asteroids[i].update_points(self), 2)

        for i in range(len(self.asteroids2)):
            if self.asteroids2[i] != None:
                pygame.draw.polygon(self.game_window, colors.get('white'), self.asteroids2[i].update_points(self), 2)

        # Lines drawn above and below "ASTEROIDS" title
        pygame.draw.line(self.game_window,colors.get('white'), 
                            (self.origin[0] - title_x_offset, self.origin[1] - self.height/4),                                                      # begin point
                            (self.origin[0] - title_x_offset + title_letter_pixel_size * title_line_length, self.origin[1] - self.height/4),        # end point
                            3)                                                                                                                      # line size
        pygame.draw.line(self.game_window,colors.get('white'), 
                            (self.origin[0] - title_x_offset, self.origin[1] - self.height/4 + title_font_size * 1.35),                                   # begin point
                            (self.origin[0] - title_x_offset + title_letter_pixel_size * title_line_length, self.origin[1] - self.height/4 + title_font_size * 1.35),    # end point
                            3)                                                                                                              # line size

        # Draw Title Text                    
        self.game_window.blit(title_text,(self.origin[0]-title_x_offset,self.origin[1] - self.height/4))

        self.game_window.blit(StartText,    (self.origin[0] - menu_x_offset_start,  self.origin[1] + self.height/4 - menu_font_size * 3))
        self.game_window.blit(OptionsText,  (self.origin[0] - menu_x_offset_options,self.origin[1] + self.height/4 - menu_font_size))
        self.game_window.blit(QuitText,     (self.origin[0] - menu_x_offset_quit,   self.origin[1] + self.height/4 + menu_font_size))

        if self.selection == 'start':
            xOffset = menu_letter_pixel_size * len(StartString) / 2
            lineLength = len(StartString)
            yOffset = -1 * menu_font_size * 3
        elif self.selection == 'options':
            xOffset = menu_letter_pixel_size * len(OptionsString) / 2
            lineLength = len(OptionsString)
            yOffset = -1 * menu_font_size
        elif self.selection == 'quit':
            xOffset = menu_letter_pixel_size * len(QuitString) / 2
            lineLength = len(QuitString)
            yOffset = menu_font_size
        
        if self.selection != None:
            pygame.draw.line(self.game_window,colors.get('white'), 
                            (self.origin[0] - xOffset, self.origin[1] + self.height/4 + yOffset),                                                       # begin point
                            (self.origin[0] - xOffset + menu_letter_pixel_size * lineLength, self.origin[1] + self.height/4 + yOffset),                        # end point
                            3)                                                                                                                          # line size
            pygame.draw.line(self.game_window,colors.get('white'), 
                            (self.origin[0] - xOffset, self.origin[1] + self.height/4 + yOffset + menu_font_size * 1.35),                                     # begin point
                            (self.origin[0] - xOffset + menu_letter_pixel_size * lineLength, self.origin[1] + self.height/4 + yOffset + menu_font_size * 1.35),      # end point
                            3)                                                                                                                          # line size

        pygame.display.update()

    def reset_game(self):
        self.player = Player(self.origin[0], self.origin[1])
        
        for i in range(len(self.asteroids)):
            self.asteroids[i] = None
        self.spawn_asteroids()
        

    def run_game_loop(self):

        while states['menu']:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if self.selection == 'start':
                            self.selection = 'options'
                        elif self.selection == 'options':
                            self.selection = 'quit'
                        elif self.selection == 'quit':
                            self.selection = 'start'
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.selection == 'start':
                            self.selection = 'quit'
                        elif self.selection == 'options':
                            self.selection = 'start'
                        elif self.selection == 'quit':
                            self.selection = 'options'
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if self.selection == 'start':
                            self.reset_game()
                            states['menu'] = False
                            states['game'] = True

            for i in range(self.num_asteroids):
                if self.asteroids[i] != None:
                    self.spawn_asteroids()

            self.asteroid_drift()
            self.draw_menu()
            self.clock.tick(self.tick_rate)

        while states['game']:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.hold_left = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.hold_right = True
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.hold_up = True
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.hold_down = True
                    elif event.key == pygame.K_SPACE:
                        self.hold_shoot = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.hold_left = False
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.hold_right = False
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.hold_up = False
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.hold_down = False
                    elif event.key == pygame.K_SPACE:
                        self.hold_shoot = False
                        self.shoot_timer = 0
            

            if self.player:
                if self.hold_up:
                    self.player.move('forward')
                if self.hold_down:
                    self.player.move('backward')
                if self.hold_left:
                    self.player.move('left')
                if self.hold_right:
                    self.player.move('right')
                if self.hold_shoot:
                    self.shoot_timer_func()
                    self.shoot_timer += (1 / self.tick_rate)

                self.player.drift(self)

            self.asteroid_drift()
            self.draw_objects()

            self.asteroid_timer_func()
            self.bullet_timer_func()
            self.check_asteroid_hit_player()
            self.check_bullet_hit()

            #SimpleTest("Talitor.png", self).run()

            self.asteroid_timer += (1 / self.tick_rate)

            self.clock.tick(self.tick_rate)

        self.run_game_loop()
