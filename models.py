import pygame
import math

from settings import *


def fps_icon(sc, clock, font):
	# clock - pg.time.Clock obj
	
	tmp_fps = str(int(clock.get_fps()))
	fps_surface_obj = pygame.Surface((27, 25)).convert()

	fps_FNT_obj = font.render(tmp_fps, 1, RED)
	fps_surface_obj.blit(fps_FNT_obj, (0, 0))
	sc.blit(fps_surface_obj, FPS_POS)

	del(fps_surface_obj)


def translate_FEN(text_fen):
	assert '/' in text_fen and 'k' in text_fen and 'K' in text_fen, 'uncorrect fen' 

	figures_map = []

	fen_rows = text_fen.split('/')
	for num_row, row  in enumerate(fen_rows):
		num_col = 1
		for char in row:
			if char.lower() in LTRS:
				figures = (char, (num_col, num_row + 1))
				figures_map.append(figures)
			if char.isdigit():
				num_col += int(char)
				continue
			num_col += 1


	return figures_map