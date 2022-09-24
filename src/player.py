import math
from math import pi

def angle(angle):
    new_angle = angle * 3.141592654 / 180
    return new_angle

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 20
        self.nose_size = 1.3
        self.rotation = 0
        self.speed = 0.1
        self.velocityX = 0
        self.velocityY = 0
        self.movement_direction = 0
        self.num_bullets = 10
        self.bullets = [None] * self.num_bullets
        self.bullet_index = 0
        self.shoot_speed = 0.3
        self.tip_point = (0,0)

    def drift(self, game):
        self.x += self.velocityX
        self.y += self.velocityY
        if self.x > game.width + self.size/2:
            self.x = 0 - self.size/2
        elif self.x < 0 - self.size/2:
            self.x = game.width + self.size/2
        if self.y > game.height + self.size/2:
            self.y = 0 - self.size/2
        elif self.y < 0 - self.size/2:
            self.y = game.height + self.size/2

        # print(self.movement_direction)

    def move(self, direction):
        if direction == 'left':
            self.rotation += 5
            if self.rotation > 360:
                self.rotation -= 360
        elif direction == 'right':
            self.rotation -= 5
            if self.rotation < 0:
                self.rotation += 360
        elif direction == 'forward':
            self.velocityX += self.speed * math.cos(angle(self.rotation))
            self.velocityY -= self.speed * math.sin(angle(self.rotation))
            if self.velocityX != 0:
                self.movement_direction = math.atan(-self.velocityY/self.velocityX) * 180 / 3.14159254

        elif direction == 'backward':
            modX = 0
            modY = 0
            if self.velocityX < 0:
                modX = 1
            elif self.velocityX > 0:
                modX = -1
            if self.velocityY < 0:
                modY = 1
            elif self.velocityY > 0:
                modY = -1
            self.velocityX += self.speed * modX
            self.velocityY += self.speed * modY

    def shoot(self):
        self.bullets[self.bullet_index] = Bullet(self)
        self.bullet_index += 1
        if self.bullet_index >=self.num_bullets:
            self.bullet_index = 0

    def generate_fire_points(self):
        point1 = self.x, self.y                                                     # vertex at center of ship

        point2 = (  self.x - ((self.size) * math.sin(angle(self.rotation - 225))) * 0.25,    # bottom left point of the ship
                    self.y - ((self.size) * math.cos(angle(self.rotation - 225))) * 0.25 )   # half the distance left point of ship

        point3 = (  self.x - 0.75 * self.size*math.cos(angle(self.rotation)),        # top middle point of the ship
                    self.y + 0.75 * self.size*math.sin(angle(self.rotation)))

        point4 = (  self.x + ((self.size) * math.sin(angle(self.rotation - 135))) * 0.25,      # bottom right point of the ship
                    self.y + ((self.size) * math.cos(angle(self.rotation - 135))) * 0.25 )     # half the distance right point of ship
        
        return (point1,point2,point3,point4)

    def generate_points(self):
        point1 = (  self.x + self.nose_size * self.size*math.cos(angle(self.rotation)),        # top middle point of the ship
                    self.y - self.nose_size * self.size*math.sin(angle(self.rotation)))
        self.tipPoint = point1

        point2 = (  self.x - (self.size) * math.sin(angle(self.rotation - 225)),    # bottom left point of the ship
                    self.y - (self.size) * math.cos(angle(self.rotation - 225)))

        point3 = (  self.x + (self.size) * math.sin(angle(self.rotation - 135)),    # bottom right point of the ship
                    self.y + (self.size) * math.cos(angle(self.rotation - 135)))
        
        point4 = (  self.x,    # ceint of the ship
                    self.y)

        return (point1,point2,point4,point3)

class Bullet:
    def __init__(self, player):
        self.x = player.tipPoint[0]
        self.y = player.tipPoint[1]
        self.size = 3
        self.speed = 10
        self.angle = player.rotation
        self.initialVelX = player.velocityX
        self.initialVelY = player.velocityY
        self.bullet_time = 0
        self.bullet_time_max = 2

    def move(self, game, player):
        # print(self.angle)
        self.x += self.initialVelX + self.speed * math.cos(self.angle*pi/180)
        self.y -= -self.initialVelY + self.speed * math.sin(self.angle*pi/180)

        if self.x > game.width + self.size:
            self.x = 0 - self.size
        elif self.x < 0 - self.size:
            self.x = game.width + self.size
        if self.y > game.height + self.size:
            self.y = 0 - self.size
        elif self.y < 0 - self.size:
            self.y = game.height + self.size
    
    def destroy(self, player, bullet_index):
        player.bullets[bullet_index] = None