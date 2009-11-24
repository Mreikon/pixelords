# -*- coding: utf-8 -*-

import pygame

import Items
import ShipTypes

# Configuration:
width = 800
height = 600
fullscreen = 0 # 0=windowed, 1=fullscreen, 2=frameless
hardwareAcceleration = False
doubleBuffer = False
scaleType = 0 # 0=pixellated, 1=smooth, 2=AdvancedMAME
scale = 1 # NOTICE: You should prefer hardware scaling
showFPS = False

gfxTheme = "default" # default, alternative
music = True
soundEffects = True
musicVolume = 0.5

playerAmount = 2

lives = 5
resetWeaponsOnDeath = True
repairKits = True

loadingSpeed = 100
shipStrenght = 100
coreLightWeapons = [Items.Cannon, Items.Shotgun, Items.Flamer, Items.Laser, Items.MachineGun, Items.Rifle, Items.Banana]
extraLightWeapons = [Items.Radiation]

coreHeavyWeapons = [Items.Bomber, Items.Backshot, Items.Reverse, Items.Dirt, Items.Halo, Items.Eraser, Items.Mine]
extraHeavyWeapons = [Items.Disruptor, Items.Larpa]

lightWeapons = coreLightWeapons #+extraLightWeapons
heavyWeapons = coreHeavyWeapons #+extraHeavyWeapons

ships = [ShipTypes.Fighter, ShipTypes.Basher, ShipTypes.Destroyer, ShipTypes.MegaGlider, ShipTypes.Interceptor, ShipTypes.Penetrator, ShipTypes.Dragon, ShipTypes.Incectar]

map = "cave" # cave, sky, house, test

# Player specific settings:

keys = []
keys.append((pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_RCTRL))
keys.append((pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_LCTRL))
keys.append((pygame.K_KP8, pygame.K_KP4, pygame.K_KP6, pygame.K_KP5, pygame.K_KP_MINUS))
keys.append((pygame.K_i, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_n))

colors = []
colors.append((255,0,0))
colors.append((0,0,255))
colors.append((0,255,0))
colors.append((0,255,255))
