import pygame
import pygame.gfxdraw

from core.tools import load_image, render_text


class Button(object):

	def __init__(self, x, y, width, height, color, text, textcolor, fontsize):

		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

		self.color = color
		self.text = text
		self.textcolor = textcolor
		self.fontsize = fontsize

		self.hitbox = self.rect

	def render(self, surface):

		text = render_text(self.text, font='arial', fontsize=self.fontsize, color=self.textcolor)

		pygame.draw.rect(surface, self.color, self.rect)
		surface.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

	def is_clicked(self, mouse_pos):

		return self.hitbox.collidepoint(mouse_pos)


class RoundedButton(Button):

	def __init__(self, x, y, width, height, color, text, textcolor, fontsize):

		super().__init__(x, y, width, height, color, text, textcolor, fontsize)

		self.radius = self.height // 2
		self.hitbox = pygame.Rect((self.x - self.radius), self.y, (self.width + 2 * self.radius), self.height)

	def render(self, surface):

		text = render_text(self.text, font='arial', fontsize=self.fontsize, color=self.textcolor)

		pygame.gfxdraw.rectangle(surface, self.rect, self.color)
		surface.fill(self.color, self.rect)
		pygame.gfxdraw.filled_circle(surface, self.x, (self.y + self.radius - 1), self.radius, self.color)
		pygame.gfxdraw.filled_circle(surface, (self.x + self.width), (self.y + self.radius - 1), self.radius, self.color)

		surface.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))


class ImageButton(object):

	def __init__(self, x, y, filename):

		self.x = x
		self.y = y

		self.image = load_image(filename)
		self.hitbox = pygame.Rect(self.x, self.y, self.image.get_rect().size[0] ,self.image.get_rect().size[1])

	def render(self, surface):

		surface.blit(self.image, (self.x, self.y))

	def is_clicked(self, mouse_pos):
		
		return self.hitbox.collidepoint(mouse_pos)


class Entry(object):

	def __init__(self, x, y, width, height, max_characters=16, color=(230, 230, 230), textcolor=(10, 10, 10)):

		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

		self.max_characters = max_characters
		self.color = color
		self.textcolor = textcolor

		self.text = ''

		self.is_active = False

	def render(self, surface):

		pygame.draw.rect(surface, self.color, self.rect)

		if self.is_active:
			pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)

		text = render_text(self.text, fontsize=20)
		surface.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

	def is_clicked(self, mouse_pos):

		if self.rect.collidepoint(mouse_pos):
			self.is_active = True

		elif not self.rect.collidepoint(mouse_pos) and self.is_active:
			self.is_active = False

	def input(self, key):

		if key == pygame.K_RETURN:
			self.is_active = False

		elif key == pygame.K_BACKSPACE:
			self.text = self.text[:-1]

		elif len(self.text) <= self.max_characters:

			if key == pygame.K_y:
				self.text += 'z'

			elif key == pygame.K_z:
				self.text += 'y'

			else:
				self.text += chr(key)

	def set_default(self, value):

		self.text = value