# -*- coding: utf-8 -*-

import pygame
import math
import random

import Settings
import Functions
import Objects
import Sound

class Weapon:
	def __init__(self, game):
		self.game = game

		self.loaded = 100.0
		self.loadSpeed = 1
		self.loading = True
		self.activationCost = 100
		self.continuousLoad = False
		self.probability = 1
		self.shotDelay = 0
		self.shotDelayVariation = 0
		self.shotDelayStatus = 0
		self.sound = None
		self.soundSingle = False

		self.recoil = 0

		self.setImage("weaponbox.png") # Use general icon when there is no weapon specific one

		self.init()

	def init(self): # Weapon specific attributes and other initializations
		pass

	def setImage(self, image): # Set weapon icon
		self.image = pygame.transform.smoothscale(pygame.image.load(Functions.gfxPath(image)).convert_alpha(), (18,18))

	def activate(self, ship): # Use the weapon
		if (not(self.loading) or self.continuousLoad) and self.loaded >= self.activationCost and self.shotDelayStatus == 0:
			if self.probability == 1 or random.uniform(0,1) < self.probability:
				self.loaded -= self.activationCost
				self.shotDelayStatus = self.shotDelay + random.randint(-self.shotDelayVariation,self.shotDelayVariation)

				self.fire(ship)

				Sound.playSound(self.game, self.sound, self.soundSingle)

				ship.dx -= self.recoil*math.cos(ship.angle)
				ship.dy -= self.recoil*math.sin(ship.angle)

		if not((not(self.loading) or self.continuousLoad) and self.loaded >= self.activationCost):
			self.loading = True
			if not(self.continuousLoad) and self.loaded >= 100:
				self.loading = False

	def fire(self, ship): # Weapon specific shoot function
		pass

	def shootObject(self, ship, object, offset, speed, speedDeviationFactor=1, spread=0, amount=1, shipSpeedEffect=1): # Spawn a new object
		for i in range(amount):
			angle = ship.angle + random.uniform(-spread,spread)
			ship.game.objects.append(object(ship.game, ship.owner, ship.x+ship.dx+offset*math.cos(angle), ship.y+ship.dy+offset*math.sin(angle),
				shipSpeedEffect*ship.dx+random.uniform(1,speedDeviationFactor)*speed*math.cos(angle), shipSpeedEffect*ship.dy+random.uniform(1,speedDeviationFactor)*speed*math.sin(angle)))

	def check(self, ship): # Per-frame checks
		if self.loading and self.loaded < 100:
			self.loaded += self.loadSpeed*(Settings.loadingSpeed/100.0)*(ship.loadingSpeed/100.0)

		if self.shotDelayStatus > 0:
			self.shotDelayStatus -= 1

class Cannon(Weapon):
	def init(self):
		self.name = "Cannon"
		self.loadSpeed = 0.75
		self.recoil = 1
		self.sound = 3

		self.setImage("cannon.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Cannonball, 12, 3)

class Missiles(Weapon):
	def init(self):
		self.name = "Missiles"
		self.loadSpeed = 0.3
		self.loading = False
		self.activationCost = 50
		self.shotDelay = 20
		self.shotDelayVariation = 2
		self.recoil = 0.2
		self.sound = 3

		self.setImage("missile.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Missile, 12, 1)

class Shotgun(Weapon):
	def init(self):
		self.name = "Shotgun"
		self.loadSpeed = 1.5
		self.recoil = 0.5
		self.sound = 4

		self.setImage("shotgun_icon.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Bullet, 10, 3, 2, 0.1, 7)

class Banana(Weapon):
	def init(self):
		self.name = "Banana"
		self.loadSpeed = 0.5
		self.recoil = 0.2

		self.setImage("banana.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Banana, 10, 0.75, 2, 0.1, 12)

class MachineGun(Weapon):
	def init(self):
		self.name = "MachineGun"
		self.loadSpeed = 0.3
		self.loading = False
		self.recoil = 0.075
		self.activationCost = 3
		self.shotDelay = 8
		self.shotDelayVariation = 5
		self.sound = 2
		self.setImage("machinegun_icon.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Bullet, 10, 5, 1.5, 0.025)

class Flamer(Weapon):
	def init(self):
		self.name = "Flamer"
		self.loadSpeed = 0.20
		self.activationCost = 1.00
		self.continuousLoad = True
		self.probability = 0.5

		self.setImage("flamer_icon.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Flame, 12, 6, 2, 0.1)

class Laser(Weapon):
	def init(self):
		self.name = "Laser"
		self.loadSpeed = 0.25
		self.loading = False
		self.activationCost = 0.5
		self.sound = 8
		self.soundSingle = True

		self.setImage("laser_icon.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Laser, 10, 1, 1, 0.05, 1, 0)

class Rifle(Weapon):
	def init(self):
		self.name = "Rifle"
		self.loadSpeed = 0.5
		self.recoil = 2
		self.sound = 1

		self.setImage("rifle_icon.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.RifleBullet, 10, 10)

class Bomber(Weapon):
	def init(self):
		self.name = "Bomber"
		self.loadSpeed = 0.5

		self.setImage("bomb.png")

	def fire(self, ship):
		ship.game.objects.append(Objects.Bomb(ship.game, ship.owner, ship.x+ship.dx, ship.y+ship.dy+15, ship.dx, ship.dy+0.5))

class Backshot(Weapon):
	def init(self):
		self.name = "Backshot"
		self.loadSpeed = 0.5
		self.recoil = -3
		self.sound = 3
		self.setImage("backshot_icon.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Shard, -10, -3, 2, 0.2, 7)

class Reverse(Weapon):
	def init(self):
		self.name = "Reverse"
		self.loadSpeed = 0.2
		self.activationCost = 0.75
		self.continuousLoad = True
		self.recoil = 0.04
		self.setImage("reverse_icon.png")

	def fire(self, ship):
		if random.uniform(0,1) < 0.5:
			ship.game.objects.append(Objects.ThrustFlame(ship.game, ship.owner, ship.x-2*ship.dx+12*math.cos(ship.angle), ship.y-2*ship.dy+12*math.sin(ship.angle), ship.dx+1*math.cos(ship.angle), ship.dy+1*math.sin(ship.angle)))

class Dirt(Weapon):
	def init(self):
		self.name = "Dirt"
		self.loadSpeed = 1
		self.recoil = 0.15

		self.setImage("dirt.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Dirtball, 14, 3)

class Disruptor(Weapon):
	def init(self):
		self.name = "Disruptor"
		self.loadSpeed = 0.1

	def fire(self, ship):
		self.shootObject(ship, Objects.Disruptionball, 20, 5)

class Larpa(Weapon):
	def init(self):
		self.name = "Larpa"
		self.loadSpeed = 0.5

	def fire(self, ship):
		self.shootObject(ship, Objects.Larpa, 20, 5)

class Halo(Weapon):
	def init(self):
		self.name = "Halo"
		self.loadSpeed = 0.75
		self.sound = 4
		self.setImage("halo_icon.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Shard, 11, 6, 1, math.pi, 25)

class Mine(Weapon):
	def init(self):
		self.name = "Mine"
		self.loadSpeed = 0.1
		self.sound = 6

		self.setImage("mine.png")

	def fire(self, ship):
		self.shootObject(ship, Objects.Mine, -20, 0)

class Eraser(Weapon):
	def init(self):
		self.name = "Eraser"
		self.loadSpeed = 0.075
		self.continuousLoad = False
		self.setImage("eraser_icon.png")

	def fire(self, ship):
		object = Objects.Eraser(ship.game, ship.x, ship.y, ship.dx, ship.dy)
		object.owner = ship
		ship.game.objects.append(object)

class Radiation(Weapon):
     def init(self):
          self.name = "Radiation"
          self.loadSpeed = 0.3
          self.recoil = 0

     def fire(self, ship):
          self.shootObject(ship, Objects.Radiation, 20, 2)

class InstaGun(Weapon):
	def init(self):
		self.name = "InstaGun"
		self.loadSpeed = 0.5
		self.sound = 7

	def fire(self, ship):
		self.shootObject(ship, Objects.InstaRail, 10, 1, 1, 0, 1, 0)
