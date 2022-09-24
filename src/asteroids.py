import math
import random as r

class Asteroids:
    
    def __init__(self, game, size):
        self.x = 0
        self.y = 0
        self.speed = r.random() * 1.5 + 0.5
        self.velocityX = 0
        self.velocityY = 0
        self.size = size
        self.avSize = self.size * (20 + r.randint(10, 25))/3                # Size 1 low = 10, high = 15
                                                                            # Size 2 low = 20, high = 30
                                                                            # size 3 low = 30, high = 45
        self.rotation = 0
        self.direction = 0
        self.movement_direction = 0
        self.spin = 0               # -1 to 1 float to determine direction of spin
        self.spin_speed_max = 3
        self.spin_mod = 1
        flip = r.randint(0,1)
        if flip == 1:
            self.spin_mod = 1
        else:
            self.spin_mod = -1
        
        self.spin = self.spin_mod * r.random() * self.spin_speed_max

        flip = r.randint(0,1)   # flip to spawn on EITHER TOP/BOTTOM OR LEFT/RIGHT
        if flip == 1:               # TOP/BOTTOM
            flip = r.randint(0,1)   # flip to spawn somewhere in the X range of the screen
            self.x = game.origin[0] + (-1**flip) * r.random()*game.width/2
            flip = r.randint(0,1)   # flip to determine spawn on EITHER TOP OR BOTTOM
            self.y = 0 if flip == 1 else game.height
            self.direction = r.random()*120 + 30 if self.y != 0 else r.random()*120 + 210
            

        else:                           # SPAWN LEFT OR RIGHT SIDE
            flip = r.randint(0,1)       # flip to spawn somewhere in the Y range of the screen
            self.y = game.origin[1] + (-1**flip) * r.random()*game.height/2
            flip = r.randint(0,1)       # flip to determine spawn on EITHER LEFT OR RIGHT
            self.x = 0 if flip == 1 else game.width
            self.direction = r.random()*120 + 120 if self.x != 0 else r.random()*120 - 60

        self.velocityX = self.speed * math.cos(self.direction * math.pi / 180)
        self.velocityY = self.speed * math.sin(self.direction * math.pi / 180)

        self.numPoints = r.randint(8,16)
        self.randomSizes = [0] * self.numPoints
        for i in range(len(self.randomSizes)):
            self.randomSizes[i] = 0.5 + r.random()
        # print(self.randomSizes)
        self.surfacePoints = [(0,0)] * self.numPoints

    def break_apart(self, game, asteroids, asteroidIndex):
        count = 0
        countMax = 2
        for i in range(len(asteroids)):
            if count >= countMax:
                break
            if self.size-1 < 1:
                break
            if game.asteroids2[i] == None and count < countMax:
                game.asteroids2[i] = Asteroids(game,self.size-1)
                game.asteroids2[i].x = self.x
                game.asteroids2[i].y = self.y
                game.asteroids2[i].direction = (self.direction + 10 + r.random()*60) if count == 0 else (self.direction - 10 - r.random()*60)
                count += 1

        asteroids[asteroidIndex] = None

        #print(self.surfacePoints)
    def update_points(self, game):
        self.surfacePoints = []
        # print(self.randomSizes)
        for i in range(self.numPoints):
            angle = (i * 360 / self.numPoints + self.rotation) * math.pi / 180
            point = (self.x + self.avSize * self.randomSizes[i] * math.cos(angle),self.y + self.avSize * self.randomSizes[i] * math.sin(angle))
            self.surfacePoints.append(point)
        return self.surfacePoints