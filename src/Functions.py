# -*- coding: utf-8 -*-

import os

import Settings

def gfxPath(file):
	if os.path.exists(os.path.join("gfx",Settings.gfxTheme,file)):
		path = os.path.join("gfx",Settings.gfxTheme,file)
	else:
		path = os.path.join("gfx","default",file)

	return path
