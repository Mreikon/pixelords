# -*- coding: utf-8 -*-

class MessageBox:
	def __init__(self):
		self.show = 0
		self.showForce = False
		self.messages = []

	def addMessage(self, message):
		if len(self.messages) > 4:
			self.messages.pop(0)

		self.messages.append(message)
		self.show = 600

		print ":: " + message

	def draw(self, game):
		if self.show > 0 or self.showForce:
			self.show -= 1
			for i,message in enumerate(self.messages):
				game.screen.blit(game.text4.render(message, True, (255,255,255)), (5,5+i*15))

class InfoOverlay:
	def __init__(self):
		self.show = False

	def draw(self, game):
		if self.show:
			game.screen.blit(game.text3.render("Hotkeys", True, (255,255,255)), (250,20))
			game.screen.blit(game.text.render("ESC - Exit the game", True, (255,255,255)), (275,60))
			game.screen.blit(game.text.render("F1 - Show this help", True, (255,255,255)), (275,80))
			game.screen.blit(game.text.render("F5 - Toggle music", True, (255,255,255)), (275,100))
			game.screen.blit(game.text.render("F10 - Save map", True, (255,255,255)), (275,120))
			game.screen.blit(game.text.render("F11 - Take a full map screenshot", True, (255,255,255)), (275,140))
			game.screen.blit(game.text.render("F12 - Take a normal screenshot", True, (255,255,255)), (275,160))
