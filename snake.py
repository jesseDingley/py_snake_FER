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
FPS = 60
FramePerSec = pygame.time.Clock()


# colors (RGB)
GREEN = (0, 255, 0)
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







"""
GAME LOOP
"""

while True:

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
        	

  
    # get mouse position coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # be able to change shade of button when hovering over it
    for button in buttons:
    	change_btn_shade_on_hover(button, mouse_x, mouse_y)

    draw_playing_grid()
    show_score(score)

    # update the game frames
    pygame.display.update()

    # we create a limitation so that the computer will not 
    # execute the game loop as many times as it can within a second. 
    FramePerSec.tick(FPS)