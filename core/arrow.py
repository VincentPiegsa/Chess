import pygame


class Arrow(object):

	def __init__(self, start, stop, width, color):

		self.start = start
		self.stop = stop
		self.width = width

		self.color = color

	def render(self, surface):

		pygame.draw.line(surface, self.color, self.start, self.stop, self.width)