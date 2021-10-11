import math
import pygame


WIDTH = 800
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 50
FPS_POS = (WIDTH - 30, 20)

INPUTBOX_HEIGHT = 40


PATH_BG_IMG = 'assets/img/main_fon.jpg'
PATH_IMG = 'assets/img/'
PATH_FIGURES_IMG = 'assets/img/pieces/'


# chess constants
LTRS = 'abcdefghijklmnopqrstuvwxyz'
CEIL_QYT = 8 # кол-во полей в каждом ряду
CEIL_SIZE = 80 
PIECES_TYPE = {
	'k': ('King', 'b'), 'K': ('King', 'w'),
	'r': ('Rook', 'b'), 'R': ('Rook', 'w'),
	'q': ('Queen', 'b'), 'Q': ('Queen', 'w'),
	'b': ('Bishop', 'b'), 'B': ('Bishop', 'w'),
	'n': ('Knight', 'b'), 'N': ('Knight', 'w'),
	'p': ('Pawn', 'b'), 'P': ('Pawn', 'w'),
}


# colors
WHITE =(255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (155, 219, 229)
DARKGRAY = (110, 110, 110)
PURPLE = (120, 0, 120)
FOR_BlACK_FIELD = (133, 71, 35)
PICK_PIECE = (47, 122, 11)
SKYBLUE = (0, 186, 255)
TREE = (199,131,60)
INPUT_FNT_COLOR = (100, 240, 50)