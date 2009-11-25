# -*- coding: utf-8 -*-

import pygame
import random

import Settings
import Menus
import Objects
import Ship

class Player:
	def __init__(self, game, keys, color):
		self.game = game
		self.keys = keys
		self.color = color

		self.lives = Settings.lives
		self.active = True

		self.winner = False

		self.shoot1 = False
		self.shoot2 = False

		self.respawnWait = 200

		self.menuStage = 1

		self.menu = Menus.shipChooser()

	def menuCheck(self):
		if self.menuStage == 1:
			if self.menu.done:
				self.menuStage = 0
				self.shipType = self.menu.ship
				del self.menu

	def menuDraw(self, i):
		self.menu.draw(self.game, self.keys, i)

	def createShip(self):
		self.spawnMessage = True
		self.ship = Ship.Ship(self.game, 0,0,0,0, self.color)
		self.ship.setShipType(self.shipType)
		self.ship.active = False
		self.game.objects.append(self.ship)

	def check(self, game):
		if self.lives > 0:
			self.shoot()

			if not(self.ship.active):
				if self.respawnWait <= 0:
					self.respawnWait = 300
					self.spawnMessage = False

					self.ship.spawn()
				else:
					self.respawnWait -= 1

					if self.respawnWait == 299:
						self.lives -= 1

						self.spawnMessage = True
						self.shoot1 = False
						self.shoot2 = False
		else:
			self.active = False
			self.spawnMessage = False

	def shoot(self):
		if self.shoot1: # Light weapon
			self.ship.lightWeapon.activate(self.ship)

		if self.shoot2: # Heavy weapon
			self.ship.heavyWeapon.activate(self.ship)

	def drawHUD(self, map, i):
		if Settings.playerAmount == 3:
			if i == 0:
				i = 1
			elif i == 1:
				i = 0

		if self.ship.x-Settings.width/(2*Settings.playerAmount) < 0 or Settings.width > Settings.playerAmount*map.width:
			left = 0
		elif self.ship.x > map.width-Settings.width/(2*Settings.playerAmount):
			left = map.width-Settings.width/Settings.playerAmount
		else:
			left = self.ship.x-Settings.width/(2*Settings.playerAmount)

		if self.ship.y-Settings.height/2 < 0 or Settings.height > Settings.playerAmount*map.height:
			top = 0
		elif self.ship.y > map.height-Settings.height/2:
			top = map.height-Settings.height
		else:
			top = self.ship.y-Settings.height/2

		if self.ship.disruption > 0:
			if random.randint(0,10) == 0:
				self.game.screen.blit(map.screenImage, (int(i*Settings.width/Settings.playerAmount),0), ((int(left),int(top)), (Settings.width/Settings.playerAmount+1,Settings.height)))
		else:
			self.game.screen.blit(map.screenImage, (int(i*Settings.width/Settings.playerAmount),0), ((int(left),int(top)), (Settings.width/Settings.playerAmount+1,Settings.height)))

		if self.ship.active:
			if self.ship.hp > self.ship.shipModel.hp/2:
				hpcolor = (0,255,0)
			elif self.ship.hp > self.ship.shipModel.hp/6:
				hpcolor = (255,255,0)
			else:
				hpcolor = (255,0,0)
			pygame.draw.rect(self.game.screen, hpcolor, ((i*Settings.width/Settings.playerAmount,Settings.height-5),(int((self.ship.hp/self.ship.shipModel.hp)*Settings.width/Settings.playerAmount),5)))

			for a,weapon in enumerate((self.ship.lightWeapon, self.ship.heavyWeapon)):
				if weapon.loaded >= 100 or not(weapon.loading):
					loadColor = (0,0,255)
				else:
					loadColor = (0,255,255)

				pygame.draw.rect(self.game.screen, loadColor, ((i*Settings.width/Settings.playerAmount,Settings.height-15+a*5),(int(((weapon.loaded)/100)*Settings.width/Settings.playerAmount),4)))

		if i > 0:
			if Settings.playerAmount == 3 and i == 2:
				pygame.draw.line(self.game.screen, (0,0,0), (int((i-1)*Settings.width/Settings.playerAmount),0), (int((i-1)*Settings.width/Settings.playerAmount),Settings.height))
			pygame.draw.line(self.game.screen, (0,0,0), (int(i*Settings.width/Settings.playerAmount),0), (int(i*Settings.width/Settings.playerAmount),Settings.height))

		if self.spawnMessage and not(self.winner):
			self.game.screen.blit(self.game.text.render("Spawning with " + str(self.ship.lightWeapon.name) + " and " + str(self.ship.heavyWeapon.name), True, (255,0,0)), (i*Settings.width/Settings.playerAmount+50,50))
			if self.lives > 1:
				self.game.screen.blit(self.game.text.render(str(self.lives) + " lives left.", True, (0,255,0)), (i*Settings.width/Settings.playerAmount+50,70))
			else:
				self.game.screen.blit(self.game.text.render("You got no extra lives!", True, (0,255,0)), (i*Settings.width/Settings.playerAmount+50,70))

		if not(self.active):
			self.game.screen.blit(self.game.text.render("You are out!", True, (255,0,0)), (i*Settings.width/Settings.playerAmount+50,50))
		elif self.winner:
			self.game.screen.blit(self.game.text2.render("You are the winner!", True, (0,255,0)), (i*Settings.width/Settings.playerAmount+50,50))
			self.game.screen.blit(self.game.text.render("Press ESCAPE to continue...", True, (0,255,255)), (i*Settings.width/Settings.playerAmount+70,100))

	def event(self, event): # Take keyboard events
		if self.game.inMenu:
			if self.menuStage > 0:
				self.menu.event(event, self.keys)
		else:
			if event.type == pygame.KEYDOWN and event.key == self.keys[0]:
				self.ship.thrust = True
			elif event.type == pygame.KEYUP and event.key == self.keys[0]:
				self.ship.thrust = False
			elif event.type == pygame.KEYDOWN and event.key == self.keys[1]:
				self.ship.rotate = -1
			elif event.type == pygame.KEYUP and event.key == self.keys[1] and self.ship.rotate == -1:
				self.ship.rotate = 0
			elif event.type == pygame.KEYDOWN and event.key == self.keys[2]:
				self.ship.rotate = 1
			elif event.type == pygame.KEYUP and event.key == self.keys[2] and self.ship.rotate == 1:
				self.ship.rotate = 0
			elif event.type == pygame.KEYDOWN and event.key == self.keys[4]:
				self.shoot1 = True
			elif event.type == pygame.KEYUP and event.key == self.keys[4]:
				self.shoot1 = False
			elif event.type == pygame.KEYDOWN and event.key == self.keys[3]:
				self.shoot2 = True
			elif event.type == pygame.KEYUP and event.key == self.keys[3]:
				self.shoot2 = False
