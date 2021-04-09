"""
file: snake.py
goal: test out pygame
"""










"""
IMPORTS
"""

# import sys
import sys

# import pygame
import pygame
from pygame.locals import *

# random
from random import randrange










"""
NOTES
"""

"""

game coordinates:
+-------------------+
|(0,0)   (5,0)
|
|
|
|
|
|
|				(n,n)
+-------------------+

rect[x(width) ,y(height),rect_width,rect_height]

pygame.draw.rect(WINDOW,DARK_GREEN,[0,0,600,600])
the (0,0) here means the TOP LEFT CORNER of the rectangle

"""











"""
INITIALISATIONS
"""

# initialise pygame
pygame.init()


# set frames per second
FPS = 15
FramePerSec = pygame.time.Clock()


# colors (RGB)
GREEN = (0, 255, 0)
RED = (255,0,0)
BLUE = (0,0,255)
DARK_GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
LIGHT_GRAY = (170,170,170)
DARK_GRAY = (100,100,100)


# fonts
BTN_FONT = pygame.font.SysFont('Arial',35)


# button texts
BTN_QUIT = BTN_FONT.render('Quit', True, BLACK)
BTN_PLAY = BTN_FONT.render('Play', True, BLACK)
BTN_MODE_CLASSIC = BTN_FONT.render('M: Classic', True, BLACK)
BTN_MODE_FACE = BTN_FONT.render('M: Face', True, BLACK)

# game window dimensions
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900


# window title
WINDOW_TITLE = "snake"


# create game window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
WINDOW.fill(GREEN)


# set window title
pygame.display.set_caption(WINDOW_TITLE)

# the distance between the bottom of the frame and the play/quit/mode buttons
BOTTOM_BTN_CLEARANCE = 70

# draw line separating play/quit/mode buttons from game
pygame.draw.rect(WINDOW,LIGHT_GRAY,[0,WINDOW_HEIGHT-100,WINDOW_WIDTH,10])

# all buttons
buttons = ["play", "quit", "mode"]

# number of times the "m" has been hit or the mode button has been pressed)
m_count = 0

# if "classic" this means playing with keys
# if "face" this means playing with facial expressions
current_mode = "classic" # or "face"

# initialise score
score = 0

# before playing the snake can't move
snake_can_move = False








"""
CLASSES
"""

class Snake:
	def __init__(self, coords, x_direction, y_direction):
		"""
		x_direction (int): direction of snake on x axis. Ex: x_direction = 20 (means snake is moving to the right)
		y_direction (int): direction of snake on y axis. Ex: x_direction = 0 (means snake is moving horizontally)
		coords (list of (int,int)): coordinates of snake
		"""
		super(Snake, self).__init__()
		self.x_direction = x_direction
		self.y_direction = y_direction
		self.coords = coords


	def show(self):
		"""
		method to show / draw snake on screen
		"""
		for x,y in self.coords:
			# add segment to screen
			pygame.draw.rect(WINDOW,BLUE,[x,y,20,20])


	def move(self):
		"""
		method to move the snake one space
		"""
		# define position of new head of snake
		new_head = (self.coords[0][0] + self.x_direction, self.coords[0][1] + self.y_direction)

		# add new head to snake
		self.coords.insert(0,new_head)

		# remove tail
		self.coords.pop()


	def change_direction_with_keys(self,event):
		"""
		method to change direction of snake
		input: event: key pressed
		ouput (None)
		"""

		# determine the actual direction of the snake
		going_left = self.x_direction == -20;
		going_right = self.x_direction == 20;
		going_up = self.y_direction == -20;
		going_down = self.y_direction == 20;

	  	# want to go left
		if event.key == pygame.K_LEFT:
			# only possible if we're not moving horizontally
			if (not going_left) and (not going_right):
				# set direction to left
				self.x_direction = -20
				self.y_direction = 0

		# want to go right
		elif event.key == pygame.K_RIGHT:
			# only possible if we're not moving horizontally
			if (not going_left) and (not going_right):
				# set direction to left
				self.x_direction = 20
				self.y_direction = 0
				
		# want to go up
		elif event.key == pygame.K_UP:
			# only possible if we're not moving vertically
			if (not going_up) and (not going_down):
				# set direction to up
				self.x_direction = 0
				self.y_direction = -20 # ATTENTION
				
		# want to go down
		elif event.key == pygame.K_DOWN:
			# only possible if we're not moving vertically
			if (not going_up) and (not going_down):
				# set direction to down
				self.x_direction = 0
				self.y_direction = 20 # ATTENTION


	def died(self):
		"""
		method to check if snake died
		output (boolean)
		"""
		return self.hit_wall() # or ...


	def hit_wall(self):
		"""
		method to check if hit wall
		ouput (boolean)
		"""
		return self.coords[0][0] >= 700 + 100 or self.coords[0][0] <= 100 or self.coords[0][1] >= 700 + 80 or self.coords[0][1] <= 80





class Apple:
	def __init__(self, coords):
		"""
		coords: (tuple of (int,int)): coordinates of apple
		"""
		super(Apple, self).__init__()
		self.coords = coords

	def show(self):
		"""
		method to show / draw apple on screen
		"""
		x, y = self.coords
		pygame.draw.rect(WINDOW,RED,[x,y,20,20])










"""
FUNCTIONS
"""

def draw_playing_grid():
	"""
	output: (None) draws rectangle of playing grid
	"""
	pygame.draw.rect(WINDOW,DARK_GREEN,[100,80,700,700])


def draw_button(button,color):
	"""
	inputs: button: (str) which button ("play" for example) 
			color: (tuple of (int,int,int)) color of button 
	output: (None) draws rectangle of button
	"""
	if button == "play":
		# draw rect
		pygame.draw.rect(WINDOW,color,[WINDOW_WIDTH/8,WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE,200,50])
		# add "play" to play button
		WINDOW.blit(BTN_PLAY , (WINDOW_WIDTH/9+75,WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE+10))

	elif button == "quit":
		# draw rect
		pygame.draw.rect(WINDOW,color,[WINDOW_WIDTH/2-100,WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE,200,50])
		# add "quit" to quit button     
		WINDOW.blit(BTN_QUIT , (WINDOW_WIDTH/2-100+65,WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE+10))

	elif button == "mode":
		# draw rect
		pygame.draw.rect(WINDOW,color,[WINDOW_WIDTH/2+140,WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE,200,50])
		# add text to mode button
		if current_mode == "classic":
			WINDOW.blit(BTN_MODE_CLASSIC, (WINDOW_WIDTH/2+140+25,WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE+10))
		elif current_mode == "face":
			WINDOW.blit(BTN_MODE_FACE, (WINDOW_WIDTH/2+140+40,WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE+10))


def mouse_hover_over_btn(button, mouse_x,mouse_y):
	"""
	inputs: button:  (str) which button ("play" for example)
			mouse_x: (int) x coord of mouse
			mouse_y: (int) y coord of mouse

	output: (boolean) returns true if mouse is hovering over button 
	"""
	if button == "play":
		return WINDOW_WIDTH/8 <= mouse_x <= (WINDOW_WIDTH/8)+200 and WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE <= mouse_y <= (WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE)+50
	elif button == "quit":
		return WINDOW_WIDTH/2-100 <= mouse_x <= (WINDOW_WIDTH/2-100)+200 and WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE <= mouse_y <= (WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE)+50
	elif button == "mode":
		return WINDOW_WIDTH/2+140 <= mouse_x <= (WINDOW_WIDTH/2+140)+200 and WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE <= mouse_y <= (WINDOW_HEIGHT-BOTTOM_BTN_CLEARANCE)+50


def change_btn_shade_on_hover(button, mouse_x, mouse_y):
	"""
	inputs: button:  (str) which button ("play" for example)
			mouse_x: (int) x coord of mouse
			mouse_y: (int) y coord of mouse

	output: (None) If mouse hovers over a button the button will change color 
	"""
	if mouse_hover_over_btn(button, mouse_x, mouse_y):
		draw_button(button, LIGHT_GRAY)
	else:
		draw_button(button, DARK_GRAY)


def show_score(score):
	"""
	input: score: (int) the current score
	output: (None) show the current score
	"""
	score_text = BTN_FONT.render(f'Score: {score}', True, BLACK)
	WINDOW.blit(score_text, (WINDOW_WIDTH/2-60,40))


def generate_random_coords():
	"""
	output (tuple of (int, int)) : random point on grid
	"""
	return (100 + 20 * randrange(700/20),80 + 20 * randrange(700/20)) # 0 - 699 inclusive


def generate_apple_coords():
	"""
	output (tuple of (int, int)) : random point on grid for apple
	"""
	apple_coords = generate_random_coords()
	if apple_coords in snake.coords:
		generate_apple_coords()
	else:
		return apple_coords


			


"""
OTHER INITS
"""

# init snake
snake = Snake([(420,400),(400,400)],20,0)
#				head      tail		x  y (direction)

# init apple
apple = Apple(generate_random_coords())



"""
GAME LOOP
"""

while True:

	# every timestep resets the number of desired changes to direction
	# (this gets incremented every timestep)
    nb_desired_changes = 0

    # check events
    for event in pygame.event.get():

        # check if we're quitting
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # mouse clicked
        if event.type == pygame.MOUSEBUTTONDOWN:

            # if quit button is clicked: exit game
            if mouse_hover_over_btn("quit", mouse_x, mouse_y):
                pygame.quit()
                sys.exit()

            # if press play btn start game
        	# if we're playing, disable p (even make btn look disabled)
            if mouse_hover_over_btn("play", mouse_x, mouse_y):
                snake_can_move = True

        	# if press mode button change mode
        	# disable m during gameplay
            if mouse_hover_over_btn("mode", mouse_x, mouse_y): # and NOT_PLAYING:
                if m_count % 2 == 0:
        			# change to face
                    current_mode = "face"
                else:
        			# change to classic
                    current_mode = "classic"

        		# increment m_count
                m_count += 1

        # key pressed
        if event.type == pygame.KEYDOWN and snake_can_move:
        	# want to change directio so add 1 (if it passes 1 then change_direction is disabled)
        	nb_desired_changes += 1
        	if nb_desired_changes == 1:
        		snake.change_direction_with_keys(event)
        	

  
    # get mouse position coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # be able to change shade of button when hovering over it
    for button in buttons:
    	change_btn_shade_on_hover(button, mouse_x, mouse_y)

    draw_playing_grid()
    show_score(score)
    snake.show()
    apple.show()

    if snake_can_move:
        snake.move()

    # snake dies
    if snake.died():
    	# reset snake
    	del snake
    	snake = Snake([(420,400),(400,400)],20,0)
    	snake_can_move = False

    	# reset apple
    	del apple
    	apple = Apple(generate_random_coords())

 



    # update the game frames
    pygame.display.update()

    # we create a limitation so that the computer will not 
    # execute the game loop as many times as it can within a second. 
    FramePerSec.tick(FPS)