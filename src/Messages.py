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
