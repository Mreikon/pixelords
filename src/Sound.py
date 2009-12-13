# -*- coding: utf-8 -*-

import pygame
import os
import random
try:
	import mutagen.oggvorbis
	mutagenEnabled = True
except:
	print "Warning: No Mutagen available, \"Now Playing\" messages won't be nice."
	mutagenEnabled = False

import Settings
import Functions

class Sound:
	def __init__(self, game):
		self.game = game

		pygame.mixer.init(44100, -16, 2, 512)

		pygame.mixer.music.set_volume(Settings.musicVolume)
		pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
		self.musicList = []

		if Settings.music:
			self.loadMusic()

		self.effects = []
		self.effects.append(pygame.mixer.Sound(os.path.join("sfx","explosion.ogg")))
		self.effects.append(pygame.mixer.Sound(os.path.join("sfx","gunshot.ogg")))
		self.effects.append(pygame.mixer.Sound(os.path.join("sfx","burst.ogg")))
		self.effects.append(pygame.mixer.Sound(os.path.join("sfx","blast.ogg")))
		self.effects.append(pygame.mixer.Sound(os.path.join("sfx","shotgun.ogg")))
		self.effects.append(pygame.mixer.Sound(os.path.join("sfx","dirt.ogg")))
		self.effects.append(pygame.mixer.Sound(os.path.join("sfx","activation.ogg")))

	def loadMusic(self):
		musicFiles = Functions.getSpecificFiles("music", "ogg")
		if len(musicFiles) > 0:
			if len(self.musicList) == 0:
				self.musicList = musicFiles
				random.shuffle(self.musicList)

			self.music = self.musicList.pop()
			pygame.mixer.music.load(self.music)
			if mutagenEnabled:
				self.game.messageBox.addMessage("Now playing: " + mutagen.oggvorbis.OggVorbis(self.music)["artist"][0] + " - " + mutagen.oggvorbis.OggVorbis(self.music)["title"][0])
			else:
				self.game.messageBox.addMessage("Now playing: " + self.music)

			pygame.mixer.music.play()
		else:
			print "Warning: No music available."

def playSound(game, number):
	if Settings.sound:
		try:
			game.sound.effects[number].play()																		
		except:
			pass
