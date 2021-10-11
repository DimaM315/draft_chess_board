import pygame
import pyperclip as clip

from settings import *
from pieces import *
from models import translate_FEN


class Board:

	def __init__(self, parent_screen, font):
		# :font - pygame.font object
		# :parent_screen - main screen pygame.display

		self.__screen = parent_screen
		self.font = font

		self.num_line = pygame.Surface((CEIL_SIZE//2-15, CEIL_SIZE*CEIL_QYT)).convert_alpha()
		self.ltrs_line = pygame.Surface((CEIL_SIZE*CEIL_QYT, CEIL_SIZE//2-15)).convert_alpha()
		self.fields = pygame.Surface((CEIL_QYT*CEIL_SIZE, CEIL_QYT*CEIL_SIZE)).convert_alpha()
		

		self.__picked_piece = None
		self.__draggon_piece = None
		self.__pressed_ceil = None
		self.inp_area = None

		self.stage = pygame.Surface((
					self.fields.get_width()+2*self.num_line.get_width(),
					self.fields.get_height() + 2*self.ltrs_line.get_height()
				)).convert_alpha()

		self.all_piecies = pygame.sprite.Group()
		self.all_ceils = pygame.sprite.Group()
		self.all_areas = pygame.sprite.Group()
		self.all_widgets = pygame.sprite.Group()

		self.before_ctrl = False # for inserting text

		self.__fill_bg()


		self.__draw_fiels_notation()	

		self.__attach_surfaces()
		self.__draw_chess_ceils()
		self.__setup_start_piecies()
		self.__setup_widgets()

		self.__grand_update()


	def __setup_widgets(self):
		self.inp_area = InputBox(self.stage, self.font)
		self.all_widgets.add(self.inp_area)


	def __draw_chess_ceils(self):
		for y in range(CEIL_QYT):
			for x in range(CEIL_QYT):
				color = WHITE if (x + y % 2) % 2 == 0 else FOR_BlACK_FIELD				
				ceil = Ceil(color, (x, y))
				self.all_ceils.add(ceil)


	def __draw_fiels_notation(self):
		for i in range(CEIL_QYT):
			num_row = self.font.render(str(8-i), 1, RED)
			self.num_line.blit(num_row, (10, i * CEIL_SIZE + CEIL_SIZE//2 - 10))
			letter_col = self.font.render(LTRS[i], 1, RED)
			self.ltrs_line.blit(letter_col, (i * CEIL_SIZE + CEIL_SIZE//2, 0))


	def __setup_start_piecies(self):
		# start position of figures on board
		figures_map = [
			('k', (5,1)), ('K', (5,8)),
			('r', (8,1)), ('R', (8,8)), 
			('r', (1,1)), ('R', (1,8)), 
			('n', (2,1)), ('N', (2,8)),
			('n', (7,1)), ('N', (7,8)),
			('b', (3,1)), ('B', (3,8)),
			('b', (6,1)), ('B', (6,8)),
			('q', (4,1)), ('Q', (4,8)),]
		pawn_map = [('p', (i+1, 2)) for i in range(8)] + \
					[('P', (i+1, 7)) for i in range(8)]

		self.__setup_board_position(figures_map+pawn_map)


	def __create_piece(self, piece_symbol:str, position:tuple):
		piece_name, piece_color = PIECES_TYPE[piece_symbol]
		piece_class = globals()[piece_name]
		return piece_class(color=piece_color, position=position)


	def __setup_board_position(self, figures_map:list):
		# setup specific chess postion, maybe particular opening, step in game
		self.all_piecies.empty()
		for ceil in self.all_ceils:
			for figures in figures_map:
				if ceil.position == figures[1]:
					figures_obj = self.__create_piece(*figures)
					figures_obj.rect = ceil.rect.copy()
					self.all_piecies.add(figures_obj)
					break


	def __fill_bg(self):
		bg_img = pygame.image.load(PATH_BG_IMG)
		bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
		self.__screen.blit(bg_img, (0, 0))
		self.stage.fill(TREE)
		self.ltrs_line.fill(TREE)
		self.num_line.fill(TREE)


	def __attach_surfaces(self):
		self.stage.blit(self.num_line, 
			(0, self.ltrs_line.get_height()))
		self.stage.blit(self.num_line, 
			(self.fields.get_width()+self.num_line.get_width(), self.ltrs_line.get_height()))
		self.stage.blit(self.ltrs_line, 
			(self.num_line.get_width(), 0))
		self.stage.blit(self.ltrs_line, 
			(self.num_line.get_width(), self.fields.get_height()+self.ltrs_line.get_height()))
		self.stage.blit(self.fields, 
			(self.num_line.get_width(), self.ltrs_line.get_height()))
		self.__screen.blit(self.stage, (HALF_WIDTH - self.stage.get_width()//2, HALF_HEIGHT - self.stage.get_height()//2))


	def __get_ceil(self, pos:tuple):
		for ceil in self.all_ceils:
			if ceil.rect.collidepoint(pos):
				return ceil
		return None


	def __get_piece(self, pos:tuple):
		for piece in self.all_piecies:
			if piece.rect.collidepoint(pos):
				return piece
		return None


	def mouse_btn_down(self, btn_type:int, pos:tuple):
		# зажата кнопка мыши
		self.__pressed_ceil = self.__get_ceil(pos)
		self.__draggon_piece = self.__get_piece(pos)

		if btn_type == 1 and self.inp_area.rect.collidepoint(pos):
			# inputbox has click
			self.inp_area.activate()
		elif btn_type == 1 or btn_type == 3:
			# inputbox has`t click
			self.inp_area.deactivate()

		if self.__draggon_piece is not None:
			for ceil in self.all_ceils:
				if ceil.field_name == self.__draggon_piece.field_name:
					pick = Area(ceil, 2)
					self.all_areas.add(pick)

			
	def mouse_btn_up(self, btn_type:int, pos:tuple):
		# зажатая кнопка мыши отпущена
		picked_ceil = self.__get_ceil(pos)

		if self.__draggon_piece is not None:
			self.__draggon_piece.setup_ceil(picked_ceil)
			self.__draggon_piece = None
			self.__unmark_all_ceils()

		if self.__pressed_ceil is not None and self.__pressed_ceil is picked_ceil:
			if btn_type == 3:# нажата правая кнопка мыши
				self.__marker_place(picked_ceil)
			if btn_type == 1:# нажата левая кнопка мыши
				self.__pick_ceil(picked_ceil)
		
		self.__grand_update()


	def drag(self, pos:tuple):
		# мыш движется 
		if self.__draggon_piece is not None:
			self.__draggon_piece.rect.center = pos
			self.__grand_update()



	def __marker_place(self, ceil):
		if not ceil.marked:
			area = Area(ceil, 1)
			self.all_areas.add(area)
		else:
			for area in self.all_areas:
				if area.field_name == ceil.field_name:
					area.kill()
					break
		ceil.marked ^= True


	def __grand_update(self):
		self.all_ceils.draw(self.__screen)
		self.all_areas.draw(self.__screen)
		self.all_piecies.draw(self.__screen)
		self.all_widgets.draw(self.__screen)

		pygame.display.update()


	def __pick_ceil(self, ceil):
		self.__unmark_all_ceils()		
		if self.__picked_piece is None:
			for piece in self.all_piecies:
				if piece.field_name == ceil.field_name:
					pick = Area(ceil, 2)
					self.all_areas.add(pick)
					self.__picked_piece = piece
		else:
			# need of piece`s step
			self.__picked_piece.setup_ceil(ceil)
			self.__picked_piece = None


	def __unmark_all_ceils(self):
		self.all_areas.empty()
		for ceil in self.all_ceils:
			ceil.marked = False


	def key_down(self, e):
		# клавиша клавиатуры нажата
		if self.inp_area.active:
			if e.key == pygame.K_RETURN:
				figures_map = translate_FEN(self.inp_area.text) 
				self.inp_area.text = ''
				self.__setup_board_position(figures_map)
			elif self.before_ctrl and e.key == pygame.K_v:
				self.inp_area.text += clip.paste()
			elif e.key == pygame.K_BACKSPACE:
				self.inp_area.text = self.inp_area.text[:-1]
			elif len(e.unicode) == 1: # other chars: abc+123456
				self.inp_area.text += e.unicode

			# for inserting text
			self.before_ctrl = True if e.key == pygame.K_LCTRL else False

			self.inp_area.render_text()
			self.__grand_update() 


	def key_up(self, e):
		# клавиша клавиатуры отжата
		pass




class Ceil(pygame.sprite.Sprite):

	def __init__(self, color:str, coords:tuple):
		super().__init__()

		self.position = (coords[0]+1, coords[1]+1) # (4,4) (3,1) (1,7) ...
		self.field_name = self.get_field_notation(coords[0]+1, coords[1]+1) # a3, b5, c3...

		self.x, self.y = self.get_absolute_coords(coords)
		self.color = color

		self.image = pygame.Surface((CEIL_SIZE, CEIL_SIZE))
		self.image.fill(color)
		self.rect = self.image.get_rect()

		self.marked = False

		
		self.rect.center = self.x, self.y


	def get_absolute_coords(self, coords:tuple):
		stage_offset = HALF_WIDTH - (4 * CEIL_SIZE) + (CEIL_SIZE // 2)
		return (coords[0] * CEIL_SIZE) + stage_offset, (coords[1] * CEIL_SIZE) + stage_offset


	def get_field_notation(self, coll:int, row:int):
		return LTRS[coll-1]+str(9-row)




class Area(pygame.sprite.Sprite):
	
	def __init__(self, ceil:Ceil, area_type:int):
		# :area_type if 1 - img placeholder, 2 - pick background, 3 - available ceil
		super().__init__()

		if area_type == 1:
			picture =  pygame.image.load(PATH_IMG + 'placeholder.png')
			self.image = pygame.transform.scale(picture, (CEIL_SIZE, CEIL_SIZE))
		elif area_type == 2:
			self.image = pygame.Surface((CEIL_SIZE, CEIL_SIZE))
			self.image.fill(PICK_PIECE)	
		elif area_type == 3:
			pass	
		self.rect = ceil.rect

		self.field_name = ceil.field_name



class InputBox(pygame.sprite.Sprite):
	# виджит для ввода FEN - шахматной позиции

	def __init__(self, stage, font):
		super().__init__()
		board_rect = stage.get_rect()
		self.width, height = board_rect.width, board_rect.height
		x, y = HALF_WIDTH - self.width//2, HALF_HEIGHT + height//2 + 10
		

		self.image = pygame.Surface((self.width, INPUTBOX_HEIGHT)).convert_alpha()
		self.image.fill(BLACK)
		pygame.draw.rect(self.image, WHITE, (0, 0, self.width, INPUTBOX_HEIGHT), 2)
		self.rect = pygame.Rect(x, y, self.width, INPUTBOX_HEIGHT)

		self.active = False # в активном режиме воспринимает нажатие клавиш 
		self.text = 'FEN:'
		self.font = font

		self.widget_name = 'inputbox'

		self.render_text()



	def activate(self):
		self.active = True
		pygame.draw.rect(self.image, GREEN, (0, 0, self.width, INPUTBOX_HEIGHT), 2)
		
		if self.text == "FEN:":
			self.text = ""
			self.render_text()


	def deactivate(self):
		self.active = False
		pygame.draw.rect(self.image, WHITE, (0, 0, self.width, INPUTBOX_HEIGHT), 2)


	def render_text(self):
		# complete update of widget area
		self.image.fill(BLACK)
		pygame.draw.rect(self.image, GREEN, (0, 0, self.width, INPUTBOX_HEIGHT), 2)
		FNT_obj = self.font.render(self.text, 1, RED)
		self.image.blit(FNT_obj, (5, 5))



		
