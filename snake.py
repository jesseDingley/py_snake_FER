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
BLACK = (0, 0, 0)
LIGHT_GRAY = (170,170,170)
DARK_GRAY = (100,100,100)


# fonts
BTN_FONT = pygame.font.SysFont('Arial',35)


# button texts
BTN_QUIT = BTN_FONT.render('Quit', True, BLACK)


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










"""
FUNCTIONS
"""

def draw_quit_button(color):
	"""
	input: color: color of button (tuple of (int,int,int))

	output: draws quit button
	"""
	pygame.draw.rect(WINDOW,color,[WINDOW_WIDTH/2-100,WINDOW_HEIGHT-80,200,50])


def mouse_hover_over_quit_btn(mouse_x,mouse_y):
	"""
	inputs: mouse_x: x coord of mouse (int)
			mouse_y: y coord of mouse (int)

	output: returns true if mouse is hovering over quit button (boolean)
	"""
	return WINDOW_WIDTH/2-100 <= mouse_x <= (WINDOW_WIDTH/2-100)+200 and WINDOW_HEIGHT-80 <= mouse_y <= (WINDOW_HEIGHT-80)+50











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
            if mouse_hover_over_quit_btn(mouse_x,mouse_y):
                pygame.quit()
                sys.exit()

  
    # get mouse position coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if mouse_hover_over_quit_btn(mouse_x, mouse_y):
        draw_quit_button(LIGHT_GRAY)
    else:
        draw_quit_button(DARK_GRAY)

	# add "quit" to quit button     
    WINDOW.blit(BTN_QUIT , (WINDOW_WIDTH/2-100+60,WINDOW_HEIGHT-80+10))

    # update the game frames
    pygame.display.update()

    # we create a limitation so that the computer will not 
    # execute the game loop as many times as it can within a second. 
    FramePerSec.tick(FPS)