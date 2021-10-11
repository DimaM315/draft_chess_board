import pygame

from board import Board
from settings import *
from models import *


pygame.init()
pygame.display.set_caption('CHESS')


sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FNT20 = pygame.font.SysFont('Arial', 20, bold=True)


board = Board(sc, FNT20)




pygame.display.flip()
clock.tick(FPS)





while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			board.mouse_btn_down(event.button, event.pos)
		if event.type == pygame.MOUSEBUTTONUP:
			board.mouse_btn_up(event.button, event.pos)
		if event.type == pygame.MOUSEMOTION:
			board.drag(event.pos)
		if event.type == pygame.KEYDOWN:
			board.key_down(event)
		if event.type == pygame.KEYUP:
			board.key_up(event)


	fps_icon(sc, clock, FNT20)


	pygame.display.flip()
	clock.tick(FPS)


	
