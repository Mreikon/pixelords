# -*- coding: utf-8 -*-

import pygame
import os

import Settings
import Functions

class Menu:
	def __init__(self):
		self.done = False

		self.init()

	def draw(self, game, i): # Draw the menu
		pass

	def event(self, event, keys): # Take keyboard events
		pass

class shipChooser(Menu):
	def init(self):
		self.shipNum = 0

	def event(self, event, keys):
		if event.type == pygame.KEYDOWN and event.key == keys[4]:
			self.ship = Settings.ships[self.shipNum]
			self.done = True
		elif event.type == pygame.KEYDOWN and event.key == keys[1]:
			if self.shipNum > 0:
				self.shipNum -= 1
			else:
				self.shipNum = len(Settings.ships)-1
		elif event.type == pygame.KEYDOWN and event.key == keys[2]:
			if self.shipNum < len(Settings.ships)-1:
				self.shipNum += 1
			else:
				self.shipNum = 0

	def draw(self, game, keys, i):
		if Settings.playerAmount == 3:
			if i == 0:
				i = 1
			elif i == 1:
				i = 0

		game.screen.fill((0,0,0), ((i*Settings.width/Settings.playerAmount,0),(Settings.width/Settings.playerAmount,Settings.height)))

		game.screen.blit(pygame.transform.scale(pygame.image.load(Functions.gfxPath(Settings.ships[self.shipNum]().image)), (200,150)),(i*Settings.width/Settings.playerAmount+25,25))

		game.screen.blit(game.text2.render(Settings.ships[self.shipNum]().name, True, (0,255,0)), (i*Settings.width/Settings.playerAmount+25,190))

		game.screen.blit(game.text.render("Strength:", True, (255,255,255)), (i*Settings.width/Settings.playerAmount+50,245))
		for x in range(Settings.ships[self.shipNum]().strength):
			pygame.draw.rect(game.screen, (255,0,0), ((i*Settings.width/Settings.playerAmount+x*15+75,270),(10,20)))

		game.screen.blit(game.text.render("Acceleration:", True, (255,255,255)), (i*Settings.width/Settings.playerAmount+50,295))
		for x in range(Settings.ships[self.shipNum]().acceleration):
			pygame.draw.rect(game.screen, (255,0,0), ((i*Settings.width/Settings.playerAmount+x*15+75,320),(10,20)))

		game.screen.blit(game.text.render("Loading speed:", True, (255,255,255)), (i*Settings.width/Settings.playerAmount+50,345))
		for x in range(Settings.ships[self.shipNum]().loadingSpeed):
			pygame.draw.rect(game.screen, (255,0,0), ((i*Settings.width/Settings.playerAmount+x*15+75,370),(10,20)))

		game.screen.blit(game.text3.render("Controls:", True, (0,255,0)), (i*Settings.width/Settings.playerAmount+25,400))

		game.screen.blit(game.text.render("Shoot / Select (menu)", True, (255,255,255)), (i*Settings.width/Settings.playerAmount+50,440))
		game.screen.blit(game.text.render(pygame.key.name(keys[4]).upper(), True, (255,0,0)), (i*Settings.width/Settings.playerAmount+75,460))

		game.screen.blit(game.text.render("Steer / Change item (menu)", True, (255,255,255)), (i*Settings.width/Settings.playerAmount+50,480))
		game.screen.blit(game.text.render(pygame.key.name(keys[1]).upper() + " + " + pygame.key.name(keys[2]).upper(), True, (255,0,0)), (i*Settings.width/Settings.playerAmount+75,500))

		game.screen.blit(game.text.render("Thrust", True, (255,255,255)), (i*Settings.width/Settings.playerAmount+50,520))
		game.screen.blit(game.text.render(pygame.key.name(keys[0]).upper(), True, (255,0,0)), (i*Settings.width/Settings.playerAmount+75,540))

		game.screen.blit(game.text.render("Shoot heavy weapon", True, (255,255,255)), (i*Settings.width/Settings.playerAmount+50,560))
		game.screen.blit(game.text.render(pygame.key.name(keys[3]).upper(), True, (255,0,0)), (i*Settings.width/Settings.playerAmount+75,580))

		if self.done:
			game.screen.blit(game.text2.render("Ready!", True, (0,255,255)), (i*Settings.width/Settings.playerAmount+60,25))
