# -*- coding: utf-8 -*-

import pygame
import os
import random

import Settings
import Functions

class Sound:
	def __init__(self):
		pygame.mixer.quit()
		pygame.mixer.init(44100, -16, 2, 512)

		pygame.mixer.music.set_volume(Settings.musicVolume)
		pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
		self.musicList = []

		if Settings.music:
			self.loadMusic()

		self.explosion = pygame.mixer.Sound(os.path.join("sfx","explosion.ogg"))
		self.gunShot = pygame.mixer.Sound(os.path.join("sfx","gunshot.ogg"))
		self.burst = pygame.mixer.Sound(os.path.join("sfx","burst.ogg"))
		self.blast = pygame.mixer.Sound(os.path.join("sfx","blast.ogg"))
		self.dirt = pygame.mixer.Sound(os.path.join("sfx","dirt.ogg"))
		self.activation = pygame.mixer.Sound(os.path.join("sfx","activation.ogg"))

	def loadMusic(self):
		if len(Functions.getSpecificFiles("music", "ogg")) > 0:
			if len(self.musicList) == 0:
				self.musicList = Functions.getSpecificFiles("music", "ogg")
				random.shuffle(self.musicList)

			self.music = self.musicList.pop()
			pygame.mixer.music.load(os.path.join("music",self.music))

			pygame.mixer.music.play()
		else:
			print "Warning: No music available."
