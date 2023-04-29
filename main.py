from os import system
from time import sleep
import colorama

colorama.init()

# Clear Terminal
def clear_screen():
	system('cls')

clear_screen()

# Prompt to enter valid input	
def prompt_for_valid_input():
	print("\n\t\tPlease give a valid input !")

# Get a valid integer input within the specified range		
def int_input(prompt_string,min=-10000,max=10000,display_grid=False):
	x = " "
	while type(x) == str or x < min or x > max :
		x = input(prompt_string)
		try:
			x = int(x)
			if x < min or x > max :
				clear_screen()
				if display_grid:
					display()
				prompt_for_valid_input()
		except ValueError:
			clear_screen()
			if display_grid:
				display()
			prompt_for_valid_input()
	else:
		return x

# To change the print color
class Colour:
	@staticmethod
	def red():
		print("\u001b[31m",end="")
		
	@staticmethod
	def green():
		print("\u001b[32m",end="")

	@staticmethod
	def yellow():
		print("\u001b[33m",end="")
		
	@staticmethod
	def blue():
		print("\u001b[34m",end="")
		
	@staticmethod
	def pink():
		print("\u001b[35m",end="")
		
	@staticmethod
	def lightblue():
		print("\u001b[36m",end="")
		
	@staticmethod
	def white():
		print("\u001b[37m",end="")
	
	@staticmethod
	def bg_colour():
		if Grid.current_player==1:
			Colour.red()
		elif Grid.current_player==2:
			Colour.green()
		elif Grid.current_player==3:
			Colour.yellow()
		elif Grid.current_player==4:
			Colour.blue()
		elif Grid.current_player==5:
			Colour.pink()
		elif Grid.current_player==6:
			Colour.lightblue()
	
	@staticmethod
	def cell_colour(row,col):
		if cell[row][col].holder==1:
			Colour.red()
		elif cell[row][col].holder==2:
			Colour.green()
		elif cell[row][col].holder==3:
			Colour.yellow()
		elif cell[row][col].holder==4:
			Colour.blue()
		elif cell[row][col].holder==5:
			Colour.pink()
		elif cell[row][col].holder==6:
			Colour.lightblue()

# Individual cell in the grid		
class Cell:
	def __init__(self,max_hold):
		self.max_hold = max_hold
		self.hold = 0
		self.holder=0
		self.exploding=False
		
	def reduce(self):
		self.hold-=(self.max_hold+1)
		self.exploding=True
		if self.hold==0:
			self.holder=0

# List containing all the cells
cell = []

# The grid which contains all the cells
class Grid:
	no_of_players = 0
	current_player = 0
	no_of_rows = 0
	no_of_cols = 0
	hit_count = 0
	explosion=False
	gameover=False

# Player class
class Player:
	dead_count=0
	def __init__(self):
		self.point = 0
		self.is_dead = False
	def kill(self):
		self.is_dead=True
		Player.dead_count+=1
# List containing all the players
player = []

# To create all the cell objects
def cells_init():
	cell_list=[]
	for i in range(Grid.no_of_rows):
		cell_list.append([])
		for j in range(Grid.no_of_cols):
			if i > 0 and i < Grid.no_of_rows-1 and j > 0 and j < Grid.no_of_cols-1:
				cell_list[i].append(Cell(3))
			elif (i == 0 or i == Grid.no_of_rows-1) and (j == 0 or j == Grid.no_of_cols-1):
				cell_list[i].append(Cell(1))
			else:
				cell_list[i].append(Cell(2))
			
	return cell_list

# Initialize the players
def players_init():
	player_list=[0]
	for i in range(1,Grid.no_of_players+1):
		player_list.append(Player())
	return player_list

# Initial game setup
def setup():
	Grid.no_of_players = int_input("\n  Enter the number of players (2 - 6) : ",2,6)
	Grid.no_of_rows = int_input("\n  Enter the number of rows in the grid (2 - 9) : ",2,9)
	Grid.no_of_cols = int_input("\n  Enter the number of columns in the grid (2 - 9) : ",2,9)
	global cell
	global player
	cell = cells_init()
	player = players_init()
	Grid.current_player=1
	
# Function to draw a horizontal line
def horizontal_line():
	Colour.bg_colour()
	print("_"*Grid.no_of_cols*6,end="_")
	print()

# Function to draw an empty line	
def empty_line():
	Colour.bg_colour()
	print("|     "*Grid.no_of_cols,end="|")
	print()

# Function to draw the line which tells the index of each cell
def index_line(row_index):
	Colour.bg_colour()
	for i in range(Grid.no_of_cols):
		print(f"|{row_index}{i}   ",end="")
	print("|")

# To display the cells during the first stage of explosion
def display1():
	clear_screen()
	print()
	row_index=-1
	for i in range(Grid.no_of_rows*4+1):
		print("\t    ",end="")
		if i%4==0:
			horizontal_line()
			row_index+=1
			continue
		elif i%4==1:
			for j in range(Grid.no_of_cols):
				Colour.bg_colour()
				print("|",end="")
				if cell[row_index][j].exploding and row_index>0:
					print("  O  ",end="")
				else:
					print("     ",end="")
			print("|")
			continue
		elif i%4==3:
			for j in range(Grid.no_of_cols):
				Colour.bg_colour()
				print("|",end="")
				if cell[row_index][j].exploding and row_index<Grid.no_of_rows-1:
					print("  O  ",end="")
				else:
					print("     ",end="")
			print("|")
			continue
			
		elif i%4==2:
			for j in range(Grid.no_of_cols):
				if cell[row_index][j].exploding:
					Colour.bg_colour()
					for k in range(4):
						if k==0:
							print("|",end="")
						elif k==1 and j>0:
							print("O",end="")
						elif k==2:
							print("   ",end="")
						elif k==3 and j<Grid.no_of_cols-1:
							print("O",end="")
						else:
							print(" ",end="")
				else:
					if cell[row_index][j].hold == 0:
						Colour.bg_colour()
						print("|     ",end="")
					elif cell[row_index][j].hold == 1:
						Colour.bg_colour()
						print("|",end="")
						Colour.cell_colour(row_index,j)
						print("  O  ",end="")
					else:
						for k in range(6):
							if k == 0:
								Colour.bg_colour()
								print("|",end="")
							elif k == 1:
								print(" ",end="")
							elif k == 5:
								print(" ",end="")
							elif k == 3:
								Colour.cell_colour(row_index,j)
								print("O",end="")
							
							elif k == 2:
								if cell[row_index][j].max_hold==3 and cell[row_index][j].hold>=3:
									Colour.cell_colour(row_index,j)
									print("O",end="") 
								else:
									print(" ",end="")
							elif k == 4:
								if cell[row_index][j].max_hold>1 and cell[row_index][j].hold>=2:
									Colour.cell_colour(row_index,j)
									print("O",end="")
								else:
									print(" ",end="")
			Colour.bg_colour()
			print("|")
						
# To display the cells during the second stage of explosion					
def display2():
	clear_screen()
	print()
	row_index=-1
	
	for i in range(Grid.no_of_rows*4+1):
		print("\t    ",end="")
		if i%4==0:
			row_index+=1
			for j in range(Grid.no_of_cols):
				if (row_index<Grid.no_of_rows and cell[row_index][j].exploding and row_index>0) or (row_index-1>=0 and cell[row_index-1][j].exploding and row_index<Grid.no_of_rows):
					Colour.bg_colour()
					print("___O__",end="")
				else:
					Colour.bg_colour()
					print("______",end="")
			print("_")
			continue
		elif i%4==1 or i%4==3:
			empty_line()
			continue
		elif i%4==2:
			for j in range(Grid.no_of_cols):
				if cell[row_index][j].exploding:
					Colour.bg_colour()
					if j>0:
						print("O     ",end="")
					else:
						print("|     ",end="")
				elif j>0 and cell[row_index][j-1].exploding:
					Colour.bg_colour()
					print("O",end="")
					if cell[row_index][j].hold==0:
						print("     ",end="")
					elif cell[row_index][j].hold==1:
						Colour.cell_colour(row_index,j)
						print("  O  ",end="")
					else:
						Colour.cell_colour(row_index,j)
						for i in range(1,6):
							if i==1:
								print(" ",end="")
							elif i==3:
								print("O",end="")
							elif i==5:
								print(" ",end="")
							elif i==2:
								if cell[row_index][j].hold>=3 and cell[row_index][j].max_hold==3:
									print("O",end="")
								else:
									print(" ",end="")
							elif i==4:
								if cell[row_index][j].hold>=2 and cell[row_index][j].max_hold>=2:
									print("O",end="")
								else:
									print(" ",end="")
				else:
					if cell[row_index][j].hold == 0:
						Colour.bg_colour()
						print("|     ",end="")
					elif cell[row_index][j].hold == 1:
						Colour.bg_colour()
						print("|",end="")
						Colour.cell_colour(row_index,j)
						print("  O  ",end="")
					else:
						for k in range(6):
							if k == 0:
								Colour.bg_colour()
								print("|",end="")
							elif k == 1:
								print(" ",end="")
							elif k == 5:
								print(" ",end="")
							elif k == 3:
								Colour.cell_colour(row_index,j)
								print("O",end="")
							
							elif k == 2:
								if cell[row_index][j].max_hold==3 and cell[row_index][j].hold>=3:
									Colour.cell_colour(row_index,j)
									print("O",end="") 
								else:
									print(" ",end="")
							elif k == 4:
								if cell[row_index][j].max_hold>1 and cell[row_index][j].hold>=2:
									Colour.cell_colour(row_index,j)
									print("O",end="")
								else:
									print(" ",end="")
			Colour.bg_colour()
			print("|")
			
# To display the cells during the third stage of explosion						
def display3():
	clear_screen()
	print()
	row_index=-1
	for i in range(Grid.no_of_rows*4+1):
		print("\t    ",end="")
		if i%4==0:
			row_index+=1
			horizontal_line()
			continue
		elif i%4==1:
			for j in range(Grid.no_of_cols):
				if row_index>0 and cell[row_index-1][j].exploding:
					Colour.bg_colour()
					print("|  O  ",end="")
				else:
					Colour.bg_colour()
					print("|     ",end="")
		elif i%4==3:
			for j in range(Grid.no_of_cols):
				if row_index<Grid.no_of_cols-1 and cell[row_index+1][j].exploding:
					Colour.bg_colour()
					print("|  O  ",end="")
				else:
					Colour.bg_colour()
					print("|     ",end="")
		elif i%4==2:
			for j in range(Grid.no_of_cols):
				for k in range(6):
					if k==0:
						Colour.bg_colour()
						print("|",end="")
					elif k==1:
						if j>0 and cell[row_index][j-1].exploding:
							Colour.bg_colour()
							print("O",end="")
						else:
							print(" ",end="")
					elif k==2:
						Colour.bg_colour()
						if cell[row_index][j].max_hold==3 and cell[row_index][j].hold>=3 and not cell[row_index][j].exploding:
							Colour.cell_colour(row_index,j)
							print("O",end="")
						else:
							print(" ",end="")
					elif k==3:
						Colour.cell_colour(row_index,j)
						if cell[row_index][j].hold>0 and not cell[row_index][j].exploding:
							print("O",end="")
						else:
							print(" ",end="")
					elif k==4:
						Colour.cell_colour(row_index,j)
						if cell[row_index][j].hold>=2 and cell[row_index][j].max_hold>=2 and not cell[row_index][j].exploding:
							print("O",end="")
						else:
							print(" ",end="")
					elif k==5:
						if j<Grid.no_of_cols-1 and cell[row_index][j+1].exploding:
							Colour.bg_colour()
							print("O",end="")
						else:
							print(" ",end="")
		Colour.bg_colour()
		print("|")
					
# Function to display the grid => This function calls display 1, 2 and 3				
def display():
	clear_screen()
	row_index = -1
	print()
	for i in range(Grid.no_of_rows*4+1):
		print("\t    ",end="")
		if i%4 == 0:
			row_index+=1
			horizontal_line()
			continue
		elif i%4 == 1:
			if Grid.explosion:
				empty_line()
			else:
				index_line(row_index)
			continue
		elif i%4 == 3:
			empty_line()
			continue
		elif i%4 == 2:
			for j in range(Grid.no_of_cols):
				if cell[row_index][j].hold == 0:
					Colour.bg_colour()
					print("|     ",end="")
				elif cell[row_index][j].hold == 1:
					Colour.bg_colour()
					print("|",end="")
					Colour.cell_colour(row_index,j)
					print("  O  ",end="")
				else:
					for k in range(6):
						if k == 0:
							Colour.bg_colour()
							print("|",end="")
						elif k == 1:
							print(" ",end="")
						elif k == 5:
							print(" ",end="")
						elif k == 3:
							Colour.cell_colour(row_index,j)
							print("O",end="")
							
						elif k == 2:
							if cell[row_index][j].max_hold==3 and cell[row_index][j].hold>=3:
								Colour.cell_colour(row_index,j)
								print("O",end="") 
							else:
								print(" ",end="")
						elif k == 4:
							if cell[row_index][j].max_hold>1 and cell[row_index][j].hold>=2:
								Colour.cell_colour(row_index,j)
								print("O",end="")
							else:
								print(" ",end="")
		Colour.bg_colour()
		print("|")
	
# The game logic	
def logic():
	if not Grid.gameover:
		if Grid.current_player==Grid.no_of_players:
			Grid.current_player=1
		else:
			Grid.current_player+=1
	display()

# To get input from the user and validate it
def user_input():
	while player[Grid.current_player].is_dead:
		logic()
	input_done=False
	while not input_done:
		row_col=int_input(f"\n\tPlayer{Grid.current_player} choose your cell : ",display_grid = True)
		row=row_col//10
		col=row_col%10
		if row<0 or row>Grid.no_of_rows-1 or col<0 or col>Grid.no_of_cols-1:
			display()
			print("\n\tPlease choose a valid cell!")
		elif (cell[row][col].holder!=0 and cell[row][col].holder!=Grid.current_player):
			display()
			print("\n\tPlease choose an unoccupied cell\n\tor a cell of your own!")
			
		else:
			input_done=True
	
	cell[row][col].hold+=1
	if cell[row][col].holder==0:
		player[Grid.current_player].point+=1
	cell[row][col].holder=Grid.current_player
	Grid.hit_count+=1
	return row_col

# What happens to the cell in index [row][col] during its explosion
def sub_explode(row,col):
	cell[row][col].hold+=1
	if cell[row][col].holder!=0:
		player[cell[row][col].holder].point-=1
	cell[row][col].holder=Grid.current_player
	player[cell[row][col].holder].point+=1
	if cell[row][col].hold>cell[row][col].max_hold:
		return True
	else:
		return False

# Gameover condition
def is_gameover():
	if Player.dead_count==Grid.no_of_players-1:
		return True
	else:
		return False
	
# Recursive function which causes cells to explode and trigger other explosions
def explode(cur_list):
	display()
	sleep(0.1)
	next_list=[]
	for i in cur_list:
		row=i//10
		col=i%10
		if cell[row][col].hold>cell[row][col].max_hold:
			cell[row][col].exploding=True
	display1()
	sleep(0.04)
	display2()
	sleep(0.04)
	display3()
	sleep(0.04)
	for i in cur_list:
		row=i//10
		col=i%10
		if cell[row][col].hold>cell[row][col].max_hold:
			
			if cell[row][col].hold-(cell[row][col].max_hold+1)==0:
				player[Grid.current_player].point-=1
			cell[row][col].reduce()
			if row>0:
				if sub_explode(row-1,col):
					next_list.append((row-1)*10+col)
			if row<Grid.no_of_rows-1:
				if sub_explode(row+1,col):
					next_list.append((row+1)*10+col)
			
			if col>0:
				if sub_explode(row,col-1):
					next_list.append(row*10+(col-1))
	
			if col<Grid.no_of_cols-1:
				if sub_explode(row,col+1):
					next_list.append(row*10+(col+1))
					
		for i in range(1,Grid.no_of_players+1):
			if Grid.hit_count>=i and player[i].point==0 and not player[i].is_dead:
				player[i].kill()
	for i in cur_list:
		row=i//10
		col=i%10
		cell[row][col].exploding=False
	if is_gameover():
		Grid.gameover=True
		display()
	elif len(next_list)>0:
		Grid.explosion=True
		explode(next_list)
	else:
		Grid.explosion=False
		
# The game loop
def game():
	setup()
	while not Grid.gameover:
		display()
		row_col=user_input()
		row=row_col//10
		col=row_col%10
		if cell[row][col].hold>cell[row][col].max_hold:
			cur_list=[row_col]
			explode(cur_list)
		logic()

game()