# -*- coding: utf-8 -*-

import pygame
import math
import os
import random

import Settings
import Functions
import Messages
import Objects
import Player
import Sound

class Game:
	def __init__(self): # Initialization
		self.gameOver = False

		self.initScreen()

		self.clock = pygame.time.Clock()

		pygame.font.init()

		self.text = pygame.font.Font(os.path.join("resources","LiberationSans-Bold.ttf"), 16)
		self.text2 = pygame.font.Font(os.path.join("resources","LiberationSans-Bold.ttf"), 42)
		self.text3 = pygame.font.Font(os.path.join("resources","LiberationSans-Bold.ttf"), 32)
		self.text4 = pygame.font.Font(os.path.join("resources","LiberationSans-Bold.ttf"), 12)

		self.messageBox = Messages.MessageBox()
		self.infoOverlay = Messages.InfoOverlay()

		if Settings.sound:
			self.sound = Sound.Sound(self)

		self.map = Map()

		self.objects = []
		self.players = []

		for i in range(Settings.playerAmount-1,-1,-1):
			self.players.append(Player.Player(self, Settings.keys[i], Settings.names[i], Settings.colors[i]))

		self.bonusTimer = Settings.bonusDelay

		self.run()

	def initScreen(self): # Create screen
		pygame.display.init()

		pygame.mouse.set_visible(False)

		screenFlags = []

		if Settings.fullscreen == 1:
			screenFlags.append(pygame.FULLSCREEN)
		elif Settings.fullscreen == 2:
			screenFlags.append(pygame.NOFRAME)

		if Settings.hwAcceleration:
			screenFlags.append(pygame.HWSURFACE)

		if Settings.doubleBuffering:
			screenFlags.append(pygame.DOUBLEBUF)

		screenFlagsCombined = 0
		for flag in screenFlags:
			screenFlagsCombined |= flag

		pygame.display.set_caption("War of Pixelords")
		pygame.display.set_icon(pygame.image.load(os.path.join("gfx","default","ship2.png")))

		if Settings.scale != 1:
			if Settings.scaleType == 2:
				Settings.scale = 2**int(math.log(Settings.scale,2))
			self.scaled = pygame.display.set_mode((int(Settings.scale*Settings.width), int(Settings.scale*Settings.height)), screenFlagsCombined)
			self.screen = pygame.transform.scale(self.scaled, (Settings.width, Settings.height))
		else:
			self.screen = pygame.display.set_mode((Settings.width, Settings.height), screenFlagsCombined)

	def scale(self): # Scale the screen
		if Settings.scaleType == 1:
			pygame.transform.smoothscale(self.screen, (Settings.scale*Settings.width, Settings.scale*Settings.height), self.scaled)
		elif Settings.scaleType == 2:
			tempscaler = []
			tempscaler.append(self.screen)
			for i in range(1,int(math.log(Settings.scale,2))):
				tempscaler.append(pygame.transform.scale2x(tempscaler[i-1]))
			pygame.transform.scale2x(tempscaler.pop(), self.scaled)
		else:
			pygame.transform.scale(self.screen, (int(Settings.scale*Settings.width), int(Settings.scale*Settings.height)), self.scaled)

	def handleEvents(self): # Handle keyboard events
		for event in pygame.event.get():
			# General events:
			if event.type == pygame.constants.USEREVENT:
				self.sound.loadMusic()

			# Global keys:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
				path = Functions.saveNameIncrement("screenshots", "screen", "png")
				pygame.image.save(self.screen, path)
				self.messageBox.addMessage("Screenshot saved to " + path + ".")
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
				if Settings.sound:
					if Settings.music:
						Settings.music = False
						pygame.mixer.music.stop()
					else:
						Settings.music = True
						self.sound.loadMusic()
				else:
					print "Warning: Can't enable music (sounds are not enabled)"
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
				if Settings.fullscreen == 1 or Settings.fullscreen == 2:
					Settings.fullscreen = 0
				elif Settings.fullscreen == 0:
					Settings.fullscreen = 1
				self.initScreen()

			# Menu keys:
			if self.inMenu:
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.running = False
					print "Terminating..."
				elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
					for player in self.players:
						player.event(event)

			# In-game keys
			else:
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.__init__()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
					self.messageBox.showForce = True
					self.infoOverlay.show = True
				elif event.type == pygame.KEYUP and event.key == pygame.K_F1:
					self.messageBox.showForce = False
					self.infoOverlay.show = False
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
					path = os.path.join("maps", "saved")
					try:
						os.mkdir(path)
					except:
						pass
					pygame.image.save(self.map.mask.make_surface(), os.path.join(path, "mask.png"))
					pygame.image.save(self.map.visual, os.path.join(path, "visual.png"))
					pygame.image.save(self.map.background.make_surface(), os.path.join(path, "background.png"))
					self.messageBox.addMessage("Current map saved to " + path + ".")
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
					path = Functions.saveNameIncrement("screenshots", "fullmap", "png")
					pygame.image.save(self.map.screenImage, path)
					self.messageBox.addMessage("Screenshot saved to " + path + ".")
				elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and not(self.gameOver):
					for player in self.players:
						if player.ship.active:
							player.event(event)

	def checkBonusSpawn(self): # Check spawn timer for repair kits and weapon changers
		if Settings.bonusDelay > 0:
			if self.bonusTimer <= 0:
				self.bonusTimer = Settings.bonusDelay
				if random.randint(0,1):
					self.objects.append(Objects.RepairKit(self, None))
					self.messageBox.addMessage("Repair kit spawned.")
				else:
					self.objects.append(Objects.WeaponChanger(self, None))
					self.messageBox.addMessage("Weapon changer spawned.")
			else:
				self.bonusTimer -= 1

	def run(self): # Main loop
		self.running = True
		self.inMenu = True

		while self.running:
			if self.inMenu:
				menuPlayers = Settings.playerAmount
				for i,player in enumerate(self.players):
					if player.menuStage == 0:
						menuPlayers -= 1
					else:
						player.menuDraw(i)
					player.menuCheck()
				if menuPlayers <= 0:
					self.inMenu = False
					self.screen.fill((0,0,0), ((0,0),(Settings.width,Settings.height)))

					self.messageBox.addMessage("Round started!")

					for player in self.players:
						player.createShip()
			else:
				for object in self.objects: # Process objects
					object.run(self.map)

				if not(self.gameOver):
					activePlayers = Settings.playerAmount
					killLimitReached = False

					for player in self.players:
						if not(player.active):
							activePlayers -= 1
						if player.kills >= Settings.killLimit:
							killLimitReached = True
							self.messageBox.addMessage(player.name + " reached the kill limit!")

						player.check(self)

					if not(Settings.insta):
						self.checkBonusSpawn()

					if activePlayers < 2 or killLimitReached:
						self.gameOver = True
						for i,player in enumerate(self.players):
							if killLimitReached and player.kills < Settings.killLimit:
								player.ship.explode(self.map)
							elif player.active:
								player.winner = True
								self.messageBox.addMessage(player.name + " is the winner!")

								player.ship.thrust = False
								player.ship.rotate = 0

				for i,player2 in enumerate(self.players): # Draw screens for each player
					player2.drawHUD(self.map, i)

				self.messageBox.draw(self)
				self.infoOverlay.draw(self)

			self.handleEvents()

			if Settings.showFPS:
				self.screen.blit(self.text.render(str(int(self.clock.get_fps())), True, (255,0,0)), (Settings.width-40,10))

			if Settings.scale != 1:
				self.scale()

			# Redraw the screen
			pygame.display.update()
			self.map.draw()

			self.clock.tick(100)

class Map:
	def __init__(self): # Load the map
		tempvisual = pygame.image.load(os.path.join("maps",Settings.map,"visual.png")).convert_alpha()
		self.maskimage = pygame.image.load(os.path.join("maps",Settings.map,"mask.png")).convert()
		self.mask = pygame.PixelArray(self.maskimage)
		self.backgroundimage = pygame.image.load(os.path.join("maps",Settings.map,"background.jpg")).convert()
		self.background = pygame.PixelArray(self.backgroundimage)
		self.width = self.maskimage.get_width()
		self.height = self.maskimage.get_height()

		self.visual = self.backgroundimage.convert()
		self.visual.blit(tempvisual, (0,0))

		self.screenImage = self.visual.convert()

		self.redrawAreas = []

	def draw(self): # Draw screenImage
		for area in self.redrawAreas:
			self.screenImage.blit(self.visual, area[0], (area[0], area[1]))
		self.redrawAreas = []

	def redraw(self, start, end): # Collect areas that need redrawing
		self.redrawAreas.append((start, end))
