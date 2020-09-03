import os
import pygame

pygame.font.init()


def load_image(filename):

    return pygame.image.load(os.path.join('assets', filename)).convert_alpha()


def render_text(text, font='arial', fontsize=30, color=(0, 0, 0)):

    font = pygame.font.SysFont(font, fontsize)
    textbox = font.render(text, True, color)

    return textbox
