import pygame

from settings import *


class Pieces(pygame.sprite.Sprite):

	def __init__(self, color:str, position:str, name:str):
		# :color - postfix color (w or b)
		# :name - color(w or b) + postfix pieces (B,K,N,Q,P,R)
		# :position - place on playboard

		super().__init__()
		picture =  pygame.image.load(PATH_FIGURES_IMG + color + name + '.png')
		self.image = pygame.transform.scale(picture, (CEIL_SIZE, CEIL_SIZE))
		self.rect = self.image.get_rect()

		self.color = color
		self.name = color+name # bN, wN, bB, wB
		self.position = position
		
		self.field_name = LTRS[position[0]-1] + str(9-position[1])


	def setup_ceil(self, ceil):
		self.rect = ceil.rect.copy()
		self.field_name = ceil.field_name





class King(Pieces):

	def __init__(self, color:str, position:str):
		super().__init__(color, position, 'K')


class Rook(Pieces):

	def __init__(self, color:str, position:str):
		super().__init__(color, position, 'R')


class Queen(Pieces):

	def __init__(self, color:str, position:str):
		super().__init__(color, position, 'Q')


class Bishop(Pieces):

	def __init__(self, color:str, position:str):
		super().__init__(color, position, 'B')


class Knight(Pieces):

	def __init__(self, color:str, position:str):
		super().__init__(color, position, 'N')


class Pawn(Pieces):

	def __init__(self, color:str, position:str):
		super().__init__(color, position, 'P')