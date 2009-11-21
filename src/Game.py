# -*- coding: utf-8 -*-

import pygame
import math
import os

import Settings
import Objects
import Player

class Game:
	def __init__(self): # Initialization
		self.gameOver = False

		self.initScreen()

		self.clock = pygame.time.Clock()

		pygame.font.init()

		self.text = pygame.font.SysFont(os.path.join("resources","LiberationSans-Regular.ttf"), 22)
		self.text2 = pygame.font.SysFont(os.path.join("resources","LiberationSans-Regular.ttf"), 54)
		self.text3 = pygame.font.SysFont(os.path.join("resources","LiberationSans-Regular.ttf"), 42)

		if Settings.music or Settings.soundEffects:
			pygame.mixer.quit()
			pygame.mixer.init(44100, -16, 2, 512)

		if Settings.music:
			self.music = pygame.mixer.Sound(os.path.join("music","victory.ogg"))
			self.music.play(-1)

		if Settings.soundEffects:
			self.soundExplode = pygame.mixer.Sound(os.path.join("sfx","beep.ogg"))

		self.map = Map()

		self.objects = []
		self.players = []

		for i in range(Settings.playerAmount-1,-1,-1):
			self.players.append(Player.Player(self, Settings.keys[i], Settings.colors[i]))

		self.bonusTimer = 3000

		self.run()

	def initScreen(self):
		pygame.display.init()

		pygame.mouse.set_visible(False)

		screenFlags = []

		if Settings.fullscreen == 1:
			screenFlags.append(pygame.FULLSCREEN)
		elif Settings.fullscreen == 2:
			screenFlags.append(pygame.NOFRAME)

		if Settings.hardwareAcceleration:
			screenFlags.append(pygame.HWSURFACE)

		if Settings.doubleBuffer:
			screenFlags.append(pygame.DOUBLEBUF)

		screenFlagsCombined = 0
		for flag in screenFlags:
			screenFlagsCombined |= flag

		if Settings.scale != 1:
			if Settings.scaleType == 2:
				Settings.scale = 2**int(math.log(Settings.scale,2))
			self.scaled = pygame.display.set_mode((int(Settings.scale*Settings.width), int(Settings.scale*Settings.height)), screenFlagsCombined)
			self.screen = pygame.transform.scale(self.scaled, (Settings.width, Settings.height))
		else:
			self.screen = pygame.display.set_mode((Settings.width, Settings.height), screenFlagsCombined)

		pygame.display.set_caption("War of Pixelords")
		pygame.display.set_icon(pygame.image.load(os.path.join("gfx","default","ship2.png")).convert_alpha())

	def scale(self):
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
			if self.inMenu:
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.running = False
					print "Terminating..."
				elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
					for player in self.players:
						player.event(event)
			else:
				if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.__init__()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
					pygame.image.save(self.map.mask, "mask.png")
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
					pygame.image.save(self.map.visual, "visual.png")
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
					pygame.image.save(self.screen, "screen.png")
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
					pygame.image.save(self.map.screenImage, "fullmap.png")
				elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and not(self.gameOver):
					for player in self.players:
						if player.ship.active:
							player.event(event)

	def checkBonusSpawn(self):
		if Settings.repairKits:
			if self.bonusTimer <= 0:
				self.bonusTimer = 3000
				self.objects.append(Objects.RepairKit(self))
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
					for player in self.players:
						player.createShip()
			else:
				# Process objects
				for object in self.objects:
					object.run(self.map)

				if not(self.gameOver):
					activePlayers = Settings.playerAmount
					for player in self.players:
						if not(player.active):
							activePlayers -= 1

						player.check(self)

					if activePlayers < 2:
						self.gameOver = True
						for i,player in enumerate(self.players):
							if player.active:
								player.winner = True

								player.ship.thrust = False
								player.ship.rotate = 0
				# Draw screens for each player
				for i,player2 in enumerate(self.players):
					player2.drawHUD(self.map, i)
			self.handleEvents()

			self.checkBonusSpawn()

			if Settings.showFPS:
				self.screen.blit(self.text.render(str(int(self.clock.get_fps())), True, (255,0,0)), (Settings.width-40,10))

			if Settings.scale != 1:
				self.scale()

			# Redraw the screen
			pygame.display.update()
			self.map.draw()

			self.clock.tick(100)

class Map:
	def __init__(self): # Load map
		tempvisual = pygame.image.load(os.path.join("maps",Settings.map,"visual.png")).convert_alpha()
		self.mask = pygame.image.load(os.path.join("maps",Settings.map,"mask.png")).convert()
		self.background = pygame.image.load(os.path.join("maps",Settings.map,"background.png")).convert()
		self.width = self.mask.get_width()
		self.height = self.mask.get_height()

		if self.width < Settings.width or self.height < Settings.height:
			print "Warning: Support for map smaller than screen is not yet implemented."

		self.visual = self.background.convert()
		self.visual.blit(tempvisual, (0,0))

		self.screenImage = self.visual.convert()

		self.redrawAreas = []

	def draw(self): # Draw screenImage
		for area in self.redrawAreas:
			self.screenImage.blit(self.visual, area[0], (area[0], area[1]))
		self.redrawAreas = []

	def redraw(self, start, end): # Collect areas that need redrawing
		self.redrawAreas.append((start, end))
