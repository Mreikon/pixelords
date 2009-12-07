# -*- coding: utf-8 -*-

import pygame
import math
import os
import random

import Settings
import Functions
import Sound

class Object(pygame.sprite.Sprite): # Parent class for all objects
	def __init__(self, game, owner, x=0,y=0, dx=0,dy=0, color=(100,100,100)): # Give default values
		self.game = game
		self.active = True

		self.owner = owner

		self.x = x
		self.y = y
		self.oldx = x
		self.oldy = y
		self.dx = dx
		self.dy = dy
		self.angle = -math.pi/2

		self.color = color
		self.isSprite = False

		self.explosionCollision = True
		self.isShip = False

		self.hp = 2
		self.airResistance = 10
		self.gravity = True

		self.thrust = False
		self.rotate = 0

		self.init()

	def sprite(self, image):
		self.isSprite = True

		pygame.sprite.Sprite.__init__(self)

		self.baseImage = pygame.image.load(Functions.gfxPath(image)).convert_alpha()
		self.image = self.baseImage
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)

	def spriteDraw(self, map):
		if self.angle != 0:
			self.rect.center = (self.x, self.y)

			oldCenter = self.rect.center
			self.image = pygame.transform.rotate(self.baseImage, math.degrees(-self.angle+3*math.pi/2))
			self.rect = self.image.get_rect()
			self.rect.center = oldCenter

			map.redraw((int(self.oldx-self.rect.width/2),int(self.oldy-self.rect.height/2)),(self.rect.width,self.rect.height))

			self.rect.center = (self.x, self.y)
			map.screenImage.blit(self.image, self.rect)

	def draw(self, map):
		if self.isSprite:
			self.spriteDraw(map)
		else:
			map.redraw((int(self.oldx-self.size),int(self.oldy-self.size)),(2*self.size,2*self.size))
			pygame.draw.circle(map.screenImage, self.color, (int(self.x),int(self.y)), int(self.size))

	def run(self, map): # Process
		if self.active:
			if self.hp <= 0:
				self.explode(map)

			self.check(map)
			if self.active:
				self.move()
				self.draw(map)

	def check(self,map):
		pass

	def onGroundHit(self,map,x,y):
		pass

	def onBorderHit(self,map,x,y):
		self.onGroundHit(map,x,y)

	def onShipHit(self,map,ship):
		pass

	def collision(self, map): # Detect collisions
		if self.isShip:
			step = 1
		else:
			step = int(self.explosionSizeFactor*int(self.size)-1)

		xrange = []
		if self.dx > 0:
			xrange = range(int(self.x)+1, int(self.x+self.dx+1.414213562373095*self.dx/math.sqrt(self.dx**2+self.dy**2+0.01))+1, 1)
		elif self.dx < 0:
			xrange = range(int(self.x)-1, int(self.x+self.dx+1.414213562373095*self.dx/math.sqrt(self.dx**2+self.dy**2+0.01))-1, -step)
		if len(xrange) == 0:
			xrange = [int(self.x)]

		yrange = []
		if self.dy > 0:
			yrange = range(int(self.y)+1, int(self.y+self.dy+1.414213562373095*self.dy/math.sqrt(self.dx**2+self.dy**2+0.01))+1, step)
		elif self.dy < 0:
			yrange = range(int(self.y)-1, int(self.y+self.dy+1.414213562373095*self.dy/math.sqrt(self.dx**2+self.dy**2+0.01))-1, -step)
		if len(yrange) == 0:
			yrange = [int(self.y)]

		groundHit = False
		shipHit = False
		for x in xrange:
			for y in yrange:
				if not(groundHit):
					if x >= map.width or x < 0 or y >=  map.height or y < 0:
						groundHit = True
						self.onBorderHit(map,x,y)
					elif map.mask.get_at((x,y)) != (0, 0, 0, 255):
						groundHit = True
						self.onGroundHit(map,x,y)

				if not(shipHit) and not(self.isShip):
					for player in self.game.players:
						object = player.ship
						if object.active:
							distance = (player.ship.x-self.x)**2 + (player.ship.y-self.y)**2
							if distance < (self.size + player.ship.size)**2:
								shipHit = True
								self.onShipHit(map,player.ship)

	def move(self): # Move
		self.oldx = self.x # Save old location
		self.oldy = self.y

		self.x += self.dx # Calculate new location with speed
		self.y += self.dy

		if self.gravity:
			self.dy += 0.01 # Gravity

		self.dx -= self.airResistance*0.0003*self.dx**3/math.fabs(self.dx+0.0001) # Air resistance
		self.dy -= self.airResistance*0.0003*self.dy**3/math.fabs(self.dy+0.0001)

		if self.thrust: # Thrusters
			self.dx += self.acceleration*math.cos(self.angle)
			self.dy += self.acceleration*math.sin(self.angle)

		if self.rotate != 0: # Rotation
			self.angle += self.rotate*0.04

	def explode(self,map): # Explode
		size = self.explosionSizeFactor*self.size

		if Settings.sound and size > 10:
			self.playSound(self.game.sound.explosion)

		if int(self.x+size) > map.width:
			right = map.width
		else:
			right = int(self.x+size)

		if int(self.x-size) < 0:
			left = 0
		else:
			left = int(self.x-size)

		for x in range(left, right):
			if (x-self.x)/(size+0.01) >= -1:
				for y in range(int((-math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y), int((math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y)):
					if y < map.height and y >= 0:
						maskValue = map.mask.get_at((x,y))
						if maskValue != (127, 127, 127, 255) and maskValue != (255, 0, 0, 255) and maskValue != (0, 0, 0, 255):
							map.mask.set_at((x,y), (0, 0, 0))
							map.visual.set_at((x,y),map.background.get_at((x,y)))
							map.screenImage.set_at((x,y), map.background.get_at((x,y)))

		for object in self.game.objects:
			distance = (object.x-self.x)**2+(object.y-self.y)**2
			if object != self and object.explosionCollision and distance < size**2:
				object.hp -= math.sqrt((1.5*size)**2-distance)

				object.dx += 0.01*(size**2-distance)*(object.x-self.x)/math.sqrt((object.x-self.x+0.01)**2+(object.y-self.y)**2)
				object.dy += 0.01*(size**2-distance)*(object.y-self.y)/math.sqrt((object.x-self.x+0.01)**2+(object.y-self.y)**2)

		for i in range(self.explosionParticleFactor*int(self.size)):
			dx = random.uniform(-2,2)
			dy = random.uniform(-2,2)
			self.game.objects.append(Shard(self.game, self.owner, self.x+5*dx,self.y+5*dy, dx, dy))

		self.destroy(map)

	def destroy(self, map): # Delete the object
		if self.active:
			map.redraw((self.x-3*self.size-10,self.y-3*self.size-10),(3*(self.size+10),3*(self.size+10)))

			self.active = False

			self.game.objects.remove(self)

	def randomizeLocation(self, map):
		while True:
			x = random.randint(1,map.width-1)
			y = random.randint(1,map.height-1)

			if map.mask.get_at((x,y)) == (0,0,0, 255):
				break

		self.x = x
		self.y = y

	def playSound(self, sound):
		if Settings.sound:
			try:
				sound.play()
			except:
				pass

class RepairKit(Object):
	def init(self):
		self.gravity = False
		self.explosionCollision = False
		self.explosionSizeFactor = 0
		self.size = 10

		self.randomizeLocation(self.game.map)

		self.sprite("repairkit.png")

	def check(self, map):
		self.collision(map)

	def onShipHit(self,map,ship):
		if ship.hp > 3*ship.shipModel.hp/4:
			ship.hp = ship.shipModel.hp
		else:
			ship.hp += ship.shipModel.hp/4

		self.destroy(map)

class WeaponChanger(Object):
	def init(self):
		self.gravity = False
		self.explosionSizeFactor = 0
		self.size = 10
		self.heavy = random.randint(0,1)
		if self.heavy:
			self.newWeapon = Settings.heavyWeapons[random.randint(0,len(Settings.heavyWeapons)-1)](self.game)
		else:
			self.newWeapon = Settings.lightWeapons[random.randint(0,len(Settings.lightWeapons)-1)](self.game)

		self.randomizeLocation(self.game.map)

		self.sprite("weaponbox.png")

	def check(self, map):
		self.collision(map)

	def onShipHit(self,map,ship):
		if self.heavy:
			ship.heavyWeapon = self.newWeapon
		else:
			ship.lightWeapon = self.newWeapon

		self.destroy(map)

	def draw(self, map):
		self.spriteDraw(map)

		self.text = self.game.text4.render(self.newWeapon.name, True, (255,255,255))

		self.game.map.screenImage.blit(self.text, (self.x-self.text.get_width()/2-1,self.y-23))
		self.game.map.redraw((int(self.x-self.text.get_width()/2-1),int(self.y-23)),(self.text.get_width(), self.text.get_height()))

class ThrustFlame(Object):
	def init(self):
		self.airResistance = 60
		self.lifetime = 10

		self.explosionSizeFactor = 50

		self.explosionCollision = False

		self.red = random.randint(170,255)
		self.green = self.red
		self.color = (self.red, self.green, 0)
		self.size = random.randint(3,4)

	def check(self, map):
		self.size += 0.1

		self.green -= self.green/5
		self.color = (self.red, int(self.green), 0)

		if self.lifetime <= 0:
			self.destroy(map)
		else:
			self.lifetime -= 1

class Smoke(Object):
	def init(self):
		self.airResistance = 60
		self.lifetime = 20

		self.explosionSizeFactor = 50

		self.explosionCollision = False

		self.lightness = random.randint(170,255)
		self.color = (self.lightness, self.lightness, self.lightness)
		self.size = random.randint(3,4)

	def check(self, map):
		self.size += 0.2

		self.lightness -= self.lightness/10
		self.color = (self.lightness, self.lightness, self.lightness)

		if self.lifetime <= 0:
			self.destroy(map)
		else:
			self.lifetime -= 1

		self.dy -= 0.1

class Eraser(Object):
	def init(self):
		self.size = 15
		self.explosionSizeFactor = 0
		self.explosionParticleFactor = 0
		self.explosionCollision = False

		self.lifetime = 500
		self.counter = 0

		self.airResistance = 0

	def check(self, map):
		if self.lifetime <= 0 or not(self.owner.active):
			self.destroy(map)
		else:
			self.lifetime -= 1

		self.x = self.owner.x+self.owner.dx
		self.y = self.owner.y+self.owner.dy

		if self.counter <= 0:
			self.counter = 2

			size = self.size

			if int(self.x+size) > map.width:
				right = map.width
			else:
				right = int(self.x+size)

			if int(self.x-size) < 0:
				left = 0
			else:
				left = int(self.x-size)

			for x in range(left, right):
				if (x-self.x)/(size+0.01) >= -1:
					for y in range(int((-math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y), int((math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y)):
						if y < map.height and y > 0:
							maskValue = map.mask.get_at((x,y))
							if maskValue != (127, 127, 127, 255) and maskValue != (255, 0, 0, 255) and maskValue != (0, 0, 0, 255):
								map.mask.set_at((x,y), (0, 0, 0))
								map.visual.set_at((x,y),map.background.get_at((x,y)))
		else:
			self.counter -= 1

	def draw(self,map):
		map.redraw((int(self.oldx-self.size-10),int(self.oldy-self.size-10)),(2*self.size+20,2*self.size+20))

		if self.lifetime > 150:
			color = (random.randint(200,255),random.randint(0,100),0,255)
		else:
			color = (0,random.randint(0,100),random.randint(200,255),255)

		pygame.draw.circle(map.screenImage, color, (int(self.x-2*self.owner.dx),int(self.y-2*self.owner.dy)), self.size, 2)

class Flame(Object):
	def init(self):
		self.airResistance = 60
		self.lifetime = 10

		self.explosionSizeFactor = 50

		self.explosionCollision = False

		self.red = random.randint(170,255)
		self.green = self.red
		self.color = (self.red, self.green, 0)
		self.size = random.randint(3,4)

	def check(self, map):
		self.collision(map)

		self.size += 0.5

		self.green -= self.green/5
		self.color = (self.red, int(self.green), 0)

		if self.lifetime <= 0:
			self.destroy(map)
		else:
			self.lifetime -= 1

	def onShipHit(self,map,ship):
		ship.hp -= 0.75
		ship.lastHitter = self.owner
		self.destroy(map)

	def onGroundHit(self,map,x,y):
		self.x = x
		self.y = y
		self.destroy(map)

class Laser(Object):
	def init(self):
		self.size = 0
		self.explosionSizeFactor = 0
		self.explosionParticleFactor = 0
		self.airResistance = 0
		self.explosionCollision = False

	def onShipHit(self,map,ship):
		ship.hp -= 0.5
		ship.lastHitter = self.owner

	def draw(self, map):
		x = self.x
		y = self.y

		Hit = False
		while not(Hit):
			x += 5*self.dx
			y += 5*self.dy

			for player in self.game.players:
				object = player.ship
				if not(Hit) and object.active:
					distance = (player.ship.x-x)**2 + (player.ship.y-y)**2
					if distance < (player.ship.size + 2)**2:
						Hit = True
						self.onShipHit(map,player.ship)

			if x >= map.width-1 or x < 0 or y >= map.height-1 or y < 0 or map.mask.get_at((int(x),int(y))) != (0, 0, 0, 255):
				Hit = True

		pygame.draw.aaline(map.screenImage, (255,0,0,255), (self.x,self.y), (x,y))

		if self.x > x:
			x1 = x-3
			x2 = self.x+3
		else:
			x1 = self.x-3
			x2 = x+3

		if self.y > y:
			y1 = y-3
			y2 = self.y+3
		else:
			y1 = self.y-3
			y2 = y+3
		map.redraw((x1,y1),(x2-x1,y2-y1))

		self.destroy(map)

class BombParticle(Object): # Class for any kinds of bombs
	def init(self):
		self.color = (176,176,176,255)
		self.shipDamage = 0
		self.shipExplode = True

		self.init2()

	def check(self, map):
		self.collision(map)

	def onGroundHit(self,map,x,y):
		self.x = x
		self.y = y

		self.explode(map)

	def onShipHit(self,map,ship):
		ship.hp -= self.shipDamage

		ship.lastHitter = self.owner

		if self.shipExplode:
			self.onGroundHit(map,self.x,self.y)
		else:
			self.x = ship.x
			self.y = ship.y
			self.destroy(map)

class Mine(BombParticle):
	def init2(self):
		self.gravity = False
		self.explosionSizeFactor = 2.5
		self.explosionParticleFactor = 2
		self.shipDamage = 0
		self.size = 10

		self.sprite("mine.png")

	def check(self, map):
		self.dx -= self.dx/20.0
		self.dy -= self.dy/20.0

		self.collision(map)

class Cannonball(BombParticle):
	def init2(self):
		self.size = 4
		self.explosionSizeFactor = 4
		self.explosionParticleFactor = 2

		self.airResistance = 5

class Bomb(BombParticle):
	def init2(self):
		self.size = 6
		self.explosionSizeFactor = 3
		self.explosionParticleFactor = 2

		self.airResistance = 10

		self.explosionCollision = False

		self.dx += random.uniform(-0.1,0.1)

class Dirtball(BombParticle):
	def init2(self):
		self.size = 5
		self.explosionSizeFactor = 4
		self.explosionCollision = False

		self.airResistance = 5

		self.color = (170,110,10,255)

	def explode(self,map): # Make dirt
		size = self.explosionSizeFactor*self.size

		if int(self.x+size) > map.width:
			right = map.width
		else:
			right = int(self.x+size)

		if int(self.x-size) < 0:
			left = 0
		else:
			left = int(self.x-size)

		for x in range(left, right):
			if (x-self.x)/(size+0.01) >= -1:
				for y in range(int((-math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y), int((math.sin(math.acos((x-self.x)/(size+0.01)))*size)+self.y)):
					if y < map.height and y > 0:
						if map.mask.get_at((x,y)) == (0,0,0,255):
							rand = random.randint(-20,20)

							map.mask.set_at((x,y), (150,90,20,255))
							map.visual.set_at((x,y),(150+rand,90+rand,20+rand,255))
							map.screenImage.set_at((x,y),(150+rand,90+rand,20+rand,255))

		self.playSound(self.game.sound.dirt)

		self.destroy(map)

class Disruptionball(BombParticle):
	def init2(self):
		self.size = 8
		self.explosionSizeFactor = 4
		self.explosionParticleFactor = 2
		self.explosionCollision = False

		self.color = (50,200,50,255)

		self.airResistance = 5

	def onGroundHit(self,map,x,y):
		self.destroy(map)

	def onShipHit(self,map,ship):
		ship.disruption = 1000

class Larpa(BombParticle):
	def init2(self):
		self.airResistance = 5
		self.size = 8
		self.drop = 0
		self.explosionSizeFactor = 1.5
		self.explosionParticleFactor = 0

	def check(self, map):
		self.collision(map)

		if self.drop == 2:
			self.drop = 0
			self.game.objects.append(Shard(self.game,self.x+random.uniform(-self.size,self.size),self.y+random.uniform(-self.size,self.size), 0, 0))
			if self.size > 5:
				self.size -= 0.1
		else:
			self.drop += 1

	def onShipHit(self,map,ship):
		self.x = ship.x
		self.y = ship.y
		self.explode(map)

	def onGroundHit(self,map,x,y):
		if (self.x-self.oldx)**2+(self.y-self.oldy)**2 > 3**2:
			self.dx = -self.dx
			self.dy = -self.dy
		else:
			self.destroy(map)

class Radiation(BombParticle):
	def init(self):
		self.airResistance = 0
 		self.size = 14
		self.explosionSizeFactor = 1
		self.explosionParticleFactor = 0
		self.explosionCollision = False
   		self.gravity = False

	def check(self, map):
		self.collision(map)

	def onShipHit(self,map,ship):
		ship.hp -= 3

	def onGroundHit(self, map, x, y):
		if self.x <= 0 or self.y <= 0 or self.x >= map.width or self.y >= map.height:
			self.destroy(map)

class Banana(BombParticle):
	def init2(self):
		self.explosionSizeFactor = 4
		self.explosionParticleFactor = 0
		self.shipDamage = 10

		self.airResistance = 5

		self.explosionCollision = False
		self.shipExplode = False

		self.size = 2

		self.rotate = random.uniform(-4,4)

		self.sprite("banana.png")

class Bullet(BombParticle):
	def init2(self):
		self.explosionSizeFactor = 2
		self.explosionParticleFactor = 0
		self.airResistance = 5

		self.explosionCollision = False
		self.shipExplode = False

		self.size = 2
		self.shipDamage = 6

class Shard(BombParticle):
	def init2(self):
		self.explosionSizeFactor = 2
		self.explosionParticleFactor = 0
		self.airResistance = 20

		self.explosionCollision = False
		self.shipExplode = False

		self.size = random.randint(2,3)
		self.shipDamage = 2*self.size

class RifleBullet(BombParticle):
	def init2(self):
		self.explosionSizeFactor = 5
		self.explosionParticleFactor = 0
		self.airResistance = 2

		self.explosionCollision = False
		self.shipExplode = False

		self.size = 2
		self.shipDamage = 50
