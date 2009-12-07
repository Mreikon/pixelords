# -*- coding: utf-8 -*-

import pygame
import colorsys
import math
import random
import os

import Settings
import Objects

class Ship(Objects.Object): # Ship
	def init(self):
		self.size = 7
		self.explosionSizeFactor = 1.5
		self.explosionParticleFactor = 5

		self.lastHitter = None

		self.airResistance = 10

		self.thrust = False
		self.rotate = 0

		self.disruption = 0

		self.isSprite = True
		self.isShip = True

		self.lightWeapon = Settings.lightWeapons[random.randint(0,len(Settings.lightWeapons)-1)](self.game)
		self.heavyWeapon = Settings.heavyWeapons[random.randint(0,len(Settings.heavyWeapons)-1)](self.game)

	def setShipType(self, shipType):
		self.shipModel = shipType()

		self.shipModel.hp = (13*self.shipModel.strength+60)*(Settings.shipStrenght/100.0)
		self.shipModel.acceleration = 0.0045*self.shipModel.acceleration+0.022
		self.shipModel.loadingSpeed = 15*self.shipModel.loadingSpeed+40

		self.sprite(self.shipModel.image)

		for x in range(self.baseImage.get_width()):
			for y in range(self.baseImage.get_height()):
				ownhue = colorsys.rgb_to_hls(self.color[0]/255.0, self.color[1]/255.0, self.color[2]/255.0)[0]
				color = colorsys.rgb_to_hls(self.baseImage.get_at((x,y))[0]/255.0, self.baseImage.get_at((x,y))[1]/255.0, self.baseImage.get_at((x,y))[2]/255.0)

				newcolor = colorsys.hls_to_rgb(ownhue, color[1], color[2])

				self.baseImage.set_at((x,y), (newcolor[0]*255, newcolor[1]*255, newcolor[2]*255, self.baseImage.get_at((x,y))[3]))

	def spawn(self):
		self.randomizeLocation(self.game.map)

		self.dx = 0
		self.dy = 0
		self.angle = 3*math.pi/2

		self.thrust = False
		self.rotate = 0

		self.disruption = 0

		self.active = True

		self.hp = self.shipModel.hp
		self.acceleration = self.shipModel.acceleration
		self.loadingSpeed = self.shipModel.loadingSpeed

	def draw(self, map):
		map.redraw((int(self.oldx-18),int(self.oldy-18)),(36,36))

		if self.thrust:
			if random.uniform(0,1) < 0.5:
				self.game.objects.append(Objects.ThrustFlame(self.game, self.owner, self.x-2*self.dx-12*math.cos(self.angle), self.y-2*self.dy-12*math.sin(self.angle), self.dx-1*math.cos(self.angle), self.dy-1*math.sin(self.angle)))

		if self.hp < self.shipModel.hp/6:
			if random.uniform(0,1) < 0.2:
				self.game.objects.append(Objects.Smoke(self.game, self.owner, self.x, self.y))

		self.spriteDraw(map)

	def destroy(self, map):
		if self.active:
			if Settings.resetWeaponsOnDeath:
				self.lightWeapon = Settings.lightWeapons[random.randint(0,len(Settings.lightWeapons)-1)](self.game)
				self.heavyWeapon = Settings.heavyWeapons[random.randint(0,len(Settings.heavyWeapons)-1)](self.game)

			map.redraw((self.x-2*self.size-10,self.y-2*self.size-10),(2*(self.size+10),2*(self.size+10)))
			self.active = False

	def check(self, map): # Check for actions
		self.collision(map)

		if self.hp < self.shipModel.hp/6:
			self.hp -= self.shipModel.hp/10000.0

		if self.disruption > 0:
			self.disruption -= 1

		self.lightWeapon.check(self)
		self.heavyWeapon.check(self)

	def onGroundHit(self,map,x,y):
		if map.mask.get_at((x,y)) == (150,90,20,255): # Dirt
			self.dx -= self.dx/5
			self.dy -= self.dy/5 + 0.008
		elif map.mask.get_at((x,y)) == (255,0,0,255): # Insta death area
			self.explode(map)
		else:
			if self.y-self.oldy != 0:
				impact = 5*math.sqrt(self.dx**2 + self.dy**2)
				if impact > 5:
					self.hp -= impact
			self.dx = 0
			self.dy = 0

	def onBorderHit(self,map,x,y):
		self.dx = 0
		self.dy = 0
