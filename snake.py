import pygame
from pygame.locals import *
from main import *

class Snake:
	"""docstring for Snake"""
	def __init__(self, coords): # coords: list of (x,y)
		super(Snake, self).__init__()
		self.coords = coords

	def show(self):
		for x,y in self.coords:
			# add segment to screen
			pygame.draw.rect(WINDOW,RED,[x,y,10,10])

		