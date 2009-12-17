# -*- coding: utf-8 -*-

import math
import os

import Settings

def gfxPath(file): # Get path for GFX
	if os.path.exists(os.path.join("gfx",Settings.gfxTheme,file)):
		path = os.path.join("gfx",Settings.gfxTheme,file)
	else:
		path = os.path.join("gfx","default",file)

	return path

def saveNameIncrement(path, name, extension): # Get path so that it doesn't overwrite old files
	number = 1

	while os.path.exists(os.path.join(path,name+str(number)+"."+extension)):
		number += 1

	return os.path.join(path,name+str(number)+"."+extension)

def getSpecificFiles(path, extension): # Get list of files with the requested type
	fileList = []

	for root, subFolders, files in os.walk(path):
		for file in files:
			if file.endswith(extension):
				fileList.append(os.path.join(root,file))

	return fileList

def returnAngle(angle):
	while angle > 2*math.pi:
		angle -= 2*math.pi
	while angle < 0:
		angle += 2*math.pi

	return angle