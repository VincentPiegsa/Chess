import pygame

from figures import Figure, Pawn, Rook, Knight, Bishop, Queen, King
from tools import render_text


class Tile(object):

	def __init__(self, row, column, width, height, position, color):

		self.row = row
		self.column = column
		self.width = width
		self.height = height

		self.rect = pygame.Rect((position[0] + self.column * self.width), (position[1] + self.row * self.height), self.width, self.height)

		self.color = color
		self.active = False

	def __repr__(self):

		return f'Tile: ({self.row}, {self.column}) <{self.color}>'

	def render(self, surface):

		pygame.draw.rect(surface, self.color, self.rect)


class Board(object):

	def __init__(self, x, y, width, height):

		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

		self.n_tiles = 8
		self.tile_width = self.width // self.n_tiles
		self.tile_height = self.height // self.n_tiles

		self.selected_tile = None

		self.tile_map = []

		self.figure_map = [[Rook(0, 0, 'white'), Knight(0, 1, 'white'), Bishop(0, 2, 'white'), Queen(0, 3, 'white'), King(0, 4, 'white'), Bishop(0, 5, 'white'), Knight(0, 6, 'white'), Rook(0, 7, 'white')],
						   [Pawn(1, 0, 'white'), Pawn(1, 1, 'white')  , Pawn(1, 2, 'white')  , Pawn(1, 3, 'white') , Pawn(1, 4, 'white'), Pawn(1, 5, 'white')  , Pawn(1, 6, 'white')  , Pawn(1,7, 'white') ],
						   [None, None, None, None, None, None, None, None],
						   [None, None, None, None, None, None, None, None],
						   [None, None, None, None, None, None, None, None],
						   [None, None, None, None, None, None, None, None],
						   [Pawn(6, 0, 'black'), Pawn(6, 1, 'black')  , Pawn(6, 2, 'black')  , Pawn(6, 3, 'black') , Pawn(6, 4, 'black'), Pawn(6, 5, 'black')  , Pawn(6, 6, 'black')  , Pawn(6, 7, 'black') ],
						   [Rook(7, 0, 'black'), Knight(7, 1, 'black'), Bishop(7, 2, 'black'), Queen(7, 3, 'black'), King(7, 4, 'black'), Bishop(7, 5, 'black'), Knight(7, 6, 'black'), Rook(7, 7, 'black')]]

		self.populate_tile_map()

	def render(self, surface):

		pygame.draw.rect(surface, (255, 255, 255), self.rect)

		for row in range(self.n_tiles):
			for column in range(self.n_tiles):
				self.tile_map[row][column].render(surface)

		if self.selected_tile:
			paths, attack_paths = self.figure_map[self.selected_tile[0]][self.selected_tile[1]].paths(self.n_tiles, self.figure_map)
			
			for path in paths:
				tile = pygame.Surface((self.tile_width, self.tile_height))
				tile.set_alpha(0.3 * 255)
				tile.fill((0, 128, 0))

				surface.blit(tile, (self.tile_map[path[0]][path[1]].rect.left, self.tile_map[path[0]][path[1]].rect.top))

			for attack_path in attack_paths:
				tile = pygame.Surface((self.tile_width, self.tile_height))
				tile.set_alpha(0.3 * 255)
				tile.fill((255, 70, 70))

				surface.blit(tile, (self.tile_map[attack_path[0]][attack_path[1]].rect.left, self.tile_map[attack_path[0]][attack_path[1]].rect.top))

			pygame.draw.rect(surface, (255, 0, 0), self.tile_map[self.selected_tile[0]][self.selected_tile[1]].rect, 2)

		for row in range(self.n_tiles):
			for column in range(self.n_tiles):

				if self.figure_map[row][column]:
					self.figure_map[row][column].render(surface, (self.x, self.y), (self.tile_width, self.tile_height))

	def populate_tile_map(self):

		color = (255, 206, 158)

		def switch_color(color):

			if color == (255, 206, 158):
				return (209, 139, 71)

			elif color == (209, 139, 71):
				return (255, 206, 158)

		for x in range(self.n_tiles):

			row = []

			for y in range(self.n_tiles):

				row.append(Tile(x, y, self.tile_width, self.tile_height, (self.x, self.y), color))
				color = switch_color(color)

			self.tile_map.append(row)
			color = switch_color(color)

	def reset_figures(self):

		self.figure_map = [[Rook(0, 0, 'white'), Knight(0, 1, 'white'), Bishop(0, 2, 'white'), Queen(0, 3, 'white'), King(0, 4, 'white'), Bishop(0, 5, 'white'), Knight(0, 6, 'white'), Rook(0, 7, 'white')],
						   [Pawn(1, 0, 'white'), Pawn(1, 1, 'white')  , Pawn(1, 2, 'white')  , Pawn(1, 3, 'white') , Pawn(1, 4, 'white'), Pawn(1, 5, 'white')  , Pawn(1, 6, 'white')  , Pawn(1,7, 'white') ],
						   [None, None, None, None, None, None, None, None],
						   [None, None, None, None, None, None, None, None],
						   [None, None, None, None, None, None, None, None],
						   [None, None, None, None, None, None, None, None],
						   [Pawn(6, 0, 'black'), Pawn(6, 1, 'black')  , Pawn(6, 2, 'black')  , Pawn(6, 3, 'black') , Pawn(6, 4, 'black'), Pawn(6, 5, 'black')  , Pawn(6, 6, 'black')  , Pawn(6, 7, 'black') ],
						   [Rook(7, 0, 'black'), Knight(7, 1, 'black'), Bishop(7, 2, 'black'), Queen(7, 3, 'black'), King(7, 4, 'black'), Bishop(7, 5, 'black'), Knight(7, 6, 'black'), Rook(7, 7, 'black')]]

	def is_clicked(self, mouse_pos, current_player):

		mouse_x, mouse_y = mouse_pos

		mouse_x -= self.x
		mouse_y -= self.y

		index = (mouse_y // self.tile_width, mouse_x // self.tile_height)

		if index[0] >= 0 and index[0] < 8:

			if index[1] >= 0 and index[1] < 8:
				tile = index

				if not self.selected_tile and not self.tile_is_empty(tile[0], tile[1]) and self.get_figure_on_tile(tile[0], tile[1]).color == current_player.get_team():
					self.selected_tile = tile

				elif self.selected_tile:
					figure = self.figure_map[self.selected_tile[0]][self.selected_tile[1]]
					paths, attack_paths = figure.paths(self.n_tiles, self.figure_map)

					if not self.tile_is_empty(tile[0], tile[1]):

						if self.get_figure_on_tile(tile[0], tile[1]).color == current_player.get_team():
							self.selected_tile = tile

						else:

							if index in attack_paths:

								current_player.points += self.figure_map[tile[0]][tile[1]].value

								figure.move(tile[0], tile[1])
								self.figure_map[self.selected_tile[0]][self.selected_tile[1]] = None
								self.selected_tile = None
								self.figure_map[tile[0]][tile[1]] = figure

								if not figure.has_moved:
									figure.has_moved = True

								current_player.move_finished = True

					else:

						if tile in paths:
							figure.move(tile[0], tile[1])

							self.figure_map[self.selected_tile[0]][self.selected_tile[1]] = None
							self.selected_tile = None
							self.figure_map[tile[0]][tile[1]] = figure

							if not figure.has_moved:
									figure.has_moved = True

							current_player.move_finished = True

	def tile_is_empty(self, row, column):

		if self.figure_map[row][column] != None:
			return False

		return True

	def get_figure_on_tile(self, row, column):

		return self.figure_map[row][column]

	def check_win_condition(self, current_player):

		if current_player.points >= 100:
			return True

		return False