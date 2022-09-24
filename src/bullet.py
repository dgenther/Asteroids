import math
from math import pi

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