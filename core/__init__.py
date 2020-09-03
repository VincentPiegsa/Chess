import datetime
import pygame
import json
import os

from board import Board
from ui_components import Button, RoundedButton, ImageButton, Entry
from tools import render_text, load_image
from player import Player

os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

pygame.init()
pygame.font.init()

config = json.load(open('config.json', 'r'))

display = pygame.display.set_mode((config['WIDTH'], config['HEIGHT']))
pygame.display.set_caption(config['TITLE'])

clock = pygame.time.Clock()

icon = load_image('icon.png')
pygame.display.set_icon(icon)

def run():

	start_menu()


def start_menu():

	def graphics(surface, entities):

		surface.fill((255, 255, 255))

		text = render_text('Chess', font='arial', fontsize=100)
		surface.blit(text, ((config['WIDTH'] - text.get_width() ) // 2, (350 - text.get_height()) // 2))

		for entity in entities:
			entity.render(surface)

	global display, clock, config

	singleplayer_button = RoundedButton(150, 350, 300, 100, (0, 0, 0), 'Singleplayer', (255, 255, 255), 40)
	multiplayer_button = RoundedButton(150, 500, 300, 100, (0, 0, 0), 'Multiplayer', (255, 255, 255), 40)
	settings_button = RoundedButton(150, 650, 300, 100, (0, 0, 0), 'Settings', (255, 255, 255), 40)

	run = True

	while run:

		clock.tick(config['FPS'])

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()

				if singleplayer_button.is_clicked(pos):
					menu_singleplayer()

				if multiplayer_button.is_clicked(pos):
					menu_multiplayer()

				if settings_button.is_clicked(pos):
					settings()

		graphics(display, [singleplayer_button, multiplayer_button, settings_button])
		pygame.display.update()


def menu_singleplayer():

	def graphics(surface, player1, player2, entities):

		display.fill((255, 255, 255))

		name = render_text('Name:')
		surface.blit(name, (50, 50))
		surface.blit(name, (350, 50))

		icon = render_text('Icon:')
		surface.blit(icon, (50, 200))
		surface.blit(icon, (350, 200))

		pygame.draw.rect(surface, (230, 230, 230), (50, 250, player1.icon_rendered.get_width(), player1.icon_rendered.get_height()), 2)
		pygame.draw.rect(surface, (230, 230, 230), (350, 250, player1.icon_rendered.get_width(), player1.icon_rendered.get_height()), 2)

		surface.blit(player1.icon_rendered, (50, 250))
		surface.blit(player2.icon_rendered, (350, 250))

		for entity in entities:
			entity.render(surface)


	global display, clock, config

	player1 = Player('Player 1', 'queen_white.png', 'white')
	player2 = Player('Player 2', 'queen_black.png', 'black')

	play_button = RoundedButton(250, 600, 100, 100, (0, 0, 0), 'Play', (255, 255, 255), 40)
	
	entry1 = Entry(50, 100, 200, 50)
	entry1.set_default(player1.name)

	entry2 = Entry(350, 100, 200, 50)
	entry2.set_default(player2.name)

	run = True

	while run:

		clock.tick(config['FPS'])

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					run = False

				if entry1.is_active:
					entry1.input(event.key)
					player1.name = entry1.text

				elif entry2.is_active:
					entry2.input(event.key)
					player2.name = entry2.text

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:
					mouse_pos = pygame.mouse.get_pos()

					entry1.is_clicked(mouse_pos)
					entry2.is_clicked(mouse_pos)

					if play_button.is_clicked(mouse_pos):
						game_singleplayer(player1, player2)

		graphics(display, player1, player2, [play_button, entry1, entry2])
		pygame.display.update()

	return


def game_singleplayer(player1, player2):

	def graphics(surface, delta_t, player1, player2, entities):

		surface.fill((255, 255, 255))

		timer = render_text('%.2d:%.2d' % (delta_t.total_seconds() // 60, delta_t.total_seconds() % 60))
		surface.blit(timer, ((config['WIDTH'] - timer.get_width()) // 2, 50))

		surface.blit(player1.name_rendered, (25, 10))
		surface.blit(player1.icon_rendered, (25, 50))

		player1_points = render_text(f'{player1.points}')
		surface.blit(player1_points, ((25 + player1.icon_rendered.get_width() + 25), 50 + (player1.icon_rendered.get_height() - player1_points.get_height()) // 2))

		surface.blit(player2.name_rendered, ((config['WIDTH'] - player2.name_rendered.get_width() - 25), 10))
		surface.blit(player2.icon_rendered, ((config['WIDTH'] - player2.icon_rendered.get_width() - 25), 50))

		player2_points = render_text(f'{player2.points}')
		surface.blit(player2_points, (((config['WIDTH'] - player2.icon_rendered.get_width()) - player2_points.get_width() - 50), 50 + (player2.icon_rendered.get_height() - player2_points.get_height()) // 2))

		for entity in entities:
			entity.render(surface)

	global display, clock, config

	board = Board(0, 200, 600, 600)

	pause_button = ImageButton(270, 25, 'pause.png')
	resume_button = ImageButton(305, 25, 'resume.png')

	start_time = datetime.datetime.now()

	player1.update()
	player2.update()

	current_player = player1

	run = True

	while run:

		clock.tick(config['FPS'])
		delta_t = datetime.datetime.now() - start_time

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					run = False

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:
					mouse_pos = pygame.mouse.get_pos()
					
					board.is_clicked(mouse_pos, current_player)

					if pause_button.is_clicked(mouse_pos):
						pass

					if resume_button.is_clicked(mouse_pos):
						pass

					if current_player.move_finished:
						current_player.move_finished = False

						if board.check_win_condition(current_player):
							return_option = game_over(current_player)

							player1.reset()
							player2.reset()

							if return_option == 'restart':
								current_player = player1
								board.reset_figures()

							elif return_option == 'quit':
								return

						if current_player == player1:
							current_player = player2

						elif current_player == player2:
							current_player = player1

		graphics(display, delta_t, player1, player2, [board, pause_button, resume_button])
		pygame.display.update()

	return


def menu_multiplayer():

	def graphics(surface, player, entities):

		surface.fill((255, 255, 255))

		profile = render_text('Profile', fontsize=40)
		surface.blit(profile, (50, 10))

		name = render_text('Name:')
		surface.blit(name, (50, 60))

		icon = render_text('Icon:')
		surface.blit(icon, (50, 160))

		surface.blit(player.icon_rendered, (50, 200))
		pygame.draw.rect(surface, (230, 230, 230), (50, 200, player.icon_rendered.get_width(), player.icon_rendered.get_height()), 2)

		connection = render_text('Connection', fontsize=40)
		surface.blit(connection, (50, 300))

		ip = render_text('IP:')
		surface.blit(ip, (50, 350))

		for entity in entities:
			entity.render(surface)

	global display, clock, config

	play_button = RoundedButton(250, 600, 100, 100, (0, 0, 0), 'Play', (255, 255, 255), 40)
	
	player = Player('Player', 'queen_black.png', 'black')

	entry1 = Entry(50, 100, 200, 50)
	entry1.set_default(player.name)

	entry2 = Entry(50, 390, 200, 50)
	entry2.set_default('127.0.0.1')

	run = True

	while run:

		clock.tick(config['FPS'])

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					run = False

				if entry1.is_active:
					entry1.input(event.key)

				if entry2.is_active:
					entry2.input(event.key)

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:
					mouse_pos = pygame.mouse.get_pos()

					entry1.is_clicked(mouse_pos)
					entry2.is_clicked(mouse_pos)

					if play_button.is_clicked(mouse_pos):
						game_multiplayer()

		graphics(display, player, [play_button, entry1, entry2])
		pygame.display.update()

	return


def game_multiplayer():

	def graphics(surface, entities):

		surface.fill((255, 255, 255))

		text = render_text('Will be added soon...', fontsize=80)
		surface.blit(text, ((config['WIDTH'] - text.get_width()) // 2, (config['HEIGHT'] - text.get_height()) // 2))

		for entity in entities:
			entity.render(surface)

	global display, clock, config
	run = True

	while run:

		clock.tick(config['FPS'])

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					run = False

		graphics(display, [])
		pygame.display.update()

	return


def settings():

	def graphics(surface, entities):

		surface.fill((255, 255, 255))

		text = render_text('Will be added soon...', fontsize=80)
		surface.blit(text, ((config['WIDTH'] - text.get_width()) // 2, (config['HEIGHT'] - text.get_height()) // 2))

		for entity in entities:
			entity.render(surface)

	global display, clock, config
	run = True

	while run:

		clock.tick(config['FPS'])

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					run = False

		graphics(display, [])
		pygame.display.update()

	return


def pause():

	def graphics(surface, entities):

		surface.fill((255, 255, 255))

		text = render_text('Will be added soon...', fontsize=80)
		surface.blit(text, ((config['WIDTH'] - text.get_width()) // 2, (config['HEIGHT'] - text.get_height()) // 2))

		for entity in entities:
			entity.render(surface)

	global display, clock, config
	run = True

	while run:

		clock.tick(config['FPS'])

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					run = False

		graphics(display, [])
		pygame.display.update()

	return


def game_over(current_player):

	def graphics(surface, entities):

		surface.fill((255, 255, 255))

		text = render_text(f'{current_player.name} won!', fontsize=40)
		surface.blit(text, ((config['WIDTH'] - text.get_width()) // 2, 100))

		for entity in entities:
			entity.render(surface)

	global display, clock, config

	restart_button = RoundedButton(150, 400, 300, 100, (0, 0, 0), 'Restart', (255, 255, 255), 40)
	quit_button = RoundedButton(150, 550, 300, 100, (0, 0, 0), 'Quit', (255, 255, 255), 40)

	run = True
	return_option = None

	while run:

		clock.tick(config['FPS'])

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					run = False

			if event.type == pygame.MOUSEBUTTONDOWN:

				if event.button == 1:
					mouse_pos = pygame.mouse.get_pos()

					if restart_button.is_clicked(mouse_pos):
						run = False
						return_option = 'restart'

					if quit_button.is_clicked(mouse_pos):
						run = False
						return_option = 'quit'

		graphics(display, [restart_button, quit_button])
		pygame.display.update()

	return return_option 


if __name__ == '__main__':

	run()
