import pygame
from tools import render_text, load_image


class Player(object):

	def __init__(self, name, icon, color):

		self.name = name
		self.icon = icon
		self.color = color
		self.points = 0
		self.move_finished = False

		self.name_rendered = render_text(self.name)
		self.icon_rendered = load_image(self.icon)

	def __repr__(self):

		return f'Player "{self.name}" ({self.color}, {self.points} Points)'

	def update(self):

		self.name_rendered = render_text(self.name)
		self.icon_rendered = load_image(self.icon)

	def get_team(self):

		return self.color

	def reset(self):
		self.points = 0
