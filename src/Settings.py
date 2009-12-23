# -*- coding: utf-8 -*-

import pygame
import ConfigParser
import os

import Weapons
import ShipTypes

config = ConfigParser.ConfigParser()
config.read("config.txt")

# Screen:
width = config.getint("Screen", "width")
height = config.getint("Screen", "height")
fullscreen = config.getint("Screen", "fullscreen")
hwAcceleration = config.getboolean("Screen", "hwAcceleration")
doubleBuffering = config.getboolean("Screen", "doubleBuffering")
scale = config.getfloat("Screen", "scaleFactor")
scaleType = config.getint("Screen", "scaleType")
showFPS = config.getboolean("Screen", "showFPS")

# Sound:
sound = config.getboolean("Sound", "enabled")
music = config.getboolean("Sound", "music")
musicVolume = config.getfloat("Sound", "musicVolume")

# Game rules:
playerAmount = config.getint("Game rules", "playerAmount")
lives = config.getint("Game rules", "lives")
killLimit = config.getint("Game rules", "killLimit")
resetWeaponsOnDeath = config.getboolean("Game rules", "resetWeaponsOnDeath")
insta = config.getboolean("Game rules", "insta")
bonusDelay = config.getint("Game rules", "bonusDelay")
loadingSpeed = config.getint("Game rules", "loadingSpeed")
shipStrength = config.getint("Game rules", "shipStrength")

map = config.get("Game rules", "map")
gfxTheme = config.get("Game rules", "gfxTheme")

coreLightWeapons = [Weapons.Cannon, Weapons.Shotgun, Weapons.Flamer, Weapons.Laser, Weapons.MachineGun, Weapons.Rifle, Weapons.Banana, Weapons.Missiles]
extraLightWeapons = [Weapons.Radiation]

coreHeavyWeapons = [Weapons.Bomber, Weapons.Backshot, Weapons.Reverse, Weapons.Dirt, Weapons.Halo, Weapons.Eraser, Weapons.Mine]
extraHeavyWeapons = [Weapons.Disruptor, Weapons.Larpa]

lightWeapons = coreLightWeapons #+extraLightWeapons
heavyWeapons = coreHeavyWeapons #+extraHeavyWeapons

if insta:
	lightWeapons = [Weapons.InstaGun]
	heavyWeapons = [Weapons.Reverse]

ships = [ShipTypes.Fighter, ShipTypes.Basher, ShipTypes.Destroyer, ShipTypes.MegaGlider, ShipTypes.Interceptor, ShipTypes.Penetrator, ShipTypes.Dragon, ShipTypes.Incectar]

# Player specific settings:
keys = []
keys.append((pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_RCTRL))
keys.append((pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_LCTRL))
keys.append((pygame.K_i, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_n))
keys.append((pygame.K_KP8, pygame.K_KP4, pygame.K_KP6, pygame.K_KP5, pygame.K_KP_MINUS))

names = []
names.append("Player 1")
names.append("Player 2")
names.append("Player 3")
names.append("Player 4")

colors = []
colors.append((255,0,0))
colors.append((0,0,255))
colors.append((0,255,0))
colors.append((0,255,255))
