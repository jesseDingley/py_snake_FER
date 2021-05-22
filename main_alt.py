"""
file: snake.py
goal: test out pygame
"""




"""
IMPORTS
"""

# import sys
import sys

import time

# import pygame
import pygame
from pygame.locals import *

# random
from random import randrange

# writing best score inside a file not accessible by the user
import shelve

# for determining if the file "best_score" already exists or not
import os.path
from os import path

# facial emotion recognition
import os
from fer import FER
import cv2
import numpy as np
# from keras.models import model_from_json
from tensorflow.compat.v1 import keras
from tensorflow.keras.preprocessing import image
import threading
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# to run FER w/ threads
config = tf.ConfigProto(
    device_count={'CPU': 1},
    intra_op_parallelism_threads=1,
    allow_soft_placement=True
)
session = tf.Session(config=config)
keras.backend.set_session(session)







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
|               (n,n)
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
NICE_GREEN = (87,138,52)
RED = (255,0,0)
BLUE = (0,0,255)
DARK_GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
LIGHT_GRAY = (170,170,170)
DARK_GRAY = (100,100,100)


# fonts
BTN_FONT = pygame.font.SysFont('arial',35)


# button texts
BTN_QUIT = BTN_FONT.render('Quit', True, BLACK)
BTN_PLAY = BTN_FONT.render('Play', True, BLACK)
BTN_OPT = BTN_FONT.render('Options', True, BLACK)
BTN_MODE_CLASSIC = BTN_FONT.render('M: Classic', True, BLACK)
BTN_MODE_FACE = BTN_FONT.render('M: Face', True, BLACK)

# game window dimensions
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900


# window title
WINDOW_TITLE = "snake"


# create game window
WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
WINDOW.fill(NICE_GREEN)


# set window title
pygame.display.set_caption(WINDOW_TITLE)

# the distance between the bottom of the frame and the play/quit/mode buttons
BOTTOM_BTN_CLEARANCE = 70

# draw line separating play/quit/mode buttons from game
pygame.draw.rect(WINDOW,LIGHT_GRAY,[0,WINDOW_HEIGHT-100,WINDOW_WIDTH,10])

# all buttons
buttons = ["play", "quit", "mode"]#, "opt"]

# number of times the "m" has been hit or the mode button has been pressed)
m_count = 0

# if "classic" this means playing with keys
# if "face" this means playing with facial expressions
current_mode = "classic" # or "face"

# initialise score
score = 0

# before playing the snake can't move
snake_can_move = False

if getattr(sys, 'frozen', False):
    wd = sys._MEIPASS
else:
    wd = ''

# snake head image
snake_head = pygame.image.load(os.path.join(wd, "images/snake_head.png"))

# background image
background = pygame.image.load(os.path.join(wd, "images/background.png"))

# apple image
apple_image = pygame.image.load(os.path.join(wd, "images/apple_image.png"))

# bomb image
bomb_image = pygame.image.load(os.path.join(wd, 'images/bomb_img2.png'))

# gold ap img
golden_apple_image = pygame.image.load(os.path.join(wd, 'images/gold_ap_img.png'))

predicted_emotion = "neutral"
nb_same_predicted_emotion = 0






"""
CLASSES
"""

class Snake:
    def __init__(self, coords, x_direction, y_direction):
        """
        x_direction (int): direction of snake on x axis. Ex: x_direction = 20 (means snake is moving to the right)
        y_direction (int): direction of snake on y axis. Ex: y_direction = 0 (means snake is moving horizontally)
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
            # i_count = 1
            if x == self.coords[0][0] and y == self.coords[0][1]:
                # draw head:

                # determine the actual direction of the snake
                going_left = self.x_direction == -20;
                going_right = self.x_direction == 20;
                going_up = self.y_direction == -20;
                going_down = self.y_direction == 20;

                draw_head = lambda rot: WINDOW.blit(pygame.transform.rotate(snake_head,rot), (x,y)) 

                if going_down:
                    draw_head(180)
                elif going_up:
                    draw_head(0)
                elif going_left:
                    draw_head(90)
                elif going_right:
                    draw_head(-90)

            else:
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

        global apple
        global golden_apple
        global score
        global best_score
        global best_score_face
        global can_show_golden_apple
        # different scenarios
        try:
            ate_apple = self.coords[0][0] == apple.coords[0] and self.coords[0][1] == apple.coords[1]
        except:
            ate_apple = False

        try:
            ate_golden_apple = self.coords[0][0] == golden_apple.coords[0] and self.coords[0][1] == golden_apple.coords[1]
        except:
            ate_golden_apple = False

        if ate_apple:
            # then dont remove tail because the snake ate an apple

            # increment score by 1
            # erase_score()
            score += 1
        

            # recalculate the best score
            best_score = max(score, best_score)
            best_score_face = max(score, best_score_face)

            # delete apple
            del apple

            # create new one
            apple = Apple(generate_apple_coords(), apple_image)

        elif ate_golden_apple and can_show_golden_apple:
            score += 5
            best_score = max(score, best_score)
            best_score_face = max(score, best_score_face)
            del golden_apple
            golden_apple = GoldenApple(generate_golden_apple_coords(), golden_apple_image)
            can_show_golden_apple = False

        else:       
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

        # print(event)

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
                # set direction to right
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


    def change_direction_with_emotion(self):
        """
        method to change direction of snake with emotion (baseline)

        ** NEUTRAl emotion means DO NOTHING **

        For now because of how bad the FER is we consider just 2 emotions
        Here's how it works:
            - if we're moving right emotion1 will make us turn left to face upwards
            - if we're moving right emotion2 will make us turn left to face downwards
            - if we're moving left emotion1 will make us turn right to face upwards
            - if w're moving left emotion2 will make us turn left to face downwards

            - if we're moving up emotion1 will make us turn
        ouput (None)

        """
        global predicted_emotion, nb_same_predicted_emotion
        # just some printings
        # print("predicted_emotion :", predicted_emotion)
        # print("nb_same_predicted_emotion :", nb_same_predicted_emotion)

        # determine the actual direction of the snake
        going_left = self.x_direction == -20;
        going_right = self.x_direction == 20;
        going_up = self.y_direction == -20;
        going_down = self.y_direction == 20;

        # sad and neutral are quite similar and interfer with each other, so if we are sad or neutral, we do nothing
        if predicted_emotion == "sad" or predicted_emotion == "neutral":
            nb_same_predicted_emotion = 0
        # happy is quite strongly isolated from the other emotions so if we are happy, we turn left
        elif predicted_emotion == "happy":
            nb_same_predicted_emotion += 1
        # angry, fear and surprise are quite hard to get so if one of them is got, then we turn right
        elif predicted_emotion in {"angry", "surprise", "fear"}:
            nb_same_predicted_emotion += 1
        else:
            nb_same_predicted_emotion = 0

        if nb_same_predicted_emotion == 1:
            # nb_same_predicted_emotion = 0
            if predicted_emotion == "happy":
                # turn left
                if going_down:
                    # right
                    e = pygame.event.Event(768, {'unicode': '', 'key': 1073741903, 'mod': 4096, 'scancode': 79, 'window': None})
                    self.change_direction_with_keys(e)
                elif going_right:
                    # up
                    e = pygame.event.Event(768, {'unicode': '', 'key': 1073741906, 'mod': 4096, 'scancode': 82, 'window': None})
                    self.change_direction_with_keys(e)
                elif going_up:
                    # left
                    e = pygame.event.Event(768, {'unicode': '', 'key': 1073741904, 'mod': 4096, 'scancode': 80, 'window': None})
                    self.change_direction_with_keys(e)
                elif going_left:
                    # down
                    e = pygame.event.Event(768, {'unicode': '', 'key': 1073741905, 'mod': 4096, 'scancode': 81, 'window': None})
                    self.change_direction_with_keys(e)
            elif predicted_emotion in {"angry", "surprise", "fear"}:
                # turn right
                if going_down:
                    # left
                    e = pygame.event.Event(768, {'unicode': '', 'key': 1073741904, 'mod': 4096, 'scancode': 80, 'window': None})
                    self.change_direction_with_keys(e)
                elif going_right:
                    # down
                    e = pygame.event.Event(768, {'unicode': '', 'key': 1073741905, 'mod': 4096, 'scancode': 81, 'window': None})
                    self.change_direction_with_keys(e)
                elif going_up:
                    # right
                    e = pygame.event.Event(768, {'unicode': '', 'key': 1073741903, 'mod': 4096, 'scancode': 79, 'window': None})
                    self.change_direction_with_keys(e)
                elif going_left:
                    # up
                    e = pygame.event.Event(768, {'unicode': '', 'key': 1073741906, 'mod': 4096, 'scancode': 82, 'window': None})
                    self.change_direction_with_keys(e)



    def died(self):
        """
        method to check if snake died
        output (boolean)
        """
        return self.hit_wall() or self.hit_self() or self.hit_bomb() # or ...


    def hit_wall(self):
        """
        method to check if hit wall
        ouput (boolean)
        """
        return self.coords[0][0] >= 700 + 100 or self.coords[0][0] < 100 or self.coords[0][1] >= 700 + 80 or self.coords[0][1] < 80


    def hit_self(self):
        """
        method to check if hit self
        """
        return self.coords[0] in self.coords[1:]


    def hit_bomb(self):
        """
        method to check if hit bomb
        """
        global bombs
        return self.coords[0] in [bomb.coords for bomb in bombs]




class Object:
    def __init__(self, coords, object_img):
        """
        coords: (tuple of (int,int)): coordinates of object
        """
        super(Object, self).__init__()
        self.coords = coords
        self.object_img = object_img

    def show(self):
        """
        method to show / draw object on screen
        """
        x, y = self.coords
        draw_object = lambda rot: WINDOW.blit(pygame.transform.rotate(self.object_img,rot), (x,y))
        # pygame.draw.rect(WINDOW,RED,[x,y,20,20])
        draw_object(0)

class GoldenApple(Object):
    pass

class Apple(Object):
    pass

class Bomb(Object):
    pass


class Checkbox:
    def __init__(self, surface, x, y, color=(230, 230, 230), caption="", outline_color=(0, 0, 0),
                 check_color=(0, 0, 0), font_size=40, font_color=(0, 0, 0), text_offset=(28, 1)):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 20, 20)
        self.checkbox_outline = self.checkbox_obj.copy()
        # variables to test the different states of the checkbox
        self.checked = False
        self.active = False
        self.unchecked = True
        self.click = False

    def _draw_button_text(self):
        self.font = pygame.font.Font(None, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + 100 / 2 - w / 2 + self.to[0], self.y + 20 / 2 - h / 2 + self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 10, self.y + 10), 8)

        elif self.unchecked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def _mouse_up(self):
            if self.active and not self.checked and self.click:
                    self.checked = True
            elif self.checked:
                self.checked = False
                self.unchecked = True

            if self.click is True and self.active is False:
                if self.checked:
                    self.checked = True
                if self.unchecked:
                    self.unchecked = True
                self.active = False

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)

    def is_checked(self):
        if self.checked is True:
            return True
        else:
            return False

    def is_unchecked(self):
        if self.checked is False:
            return True
        else:
            return False

bomb_chkbox = Checkbox(WINDOW, 100, 10, caption = "Bombs")
medium_speed_chkbox = Checkbox(WINDOW, 100, 40, caption = "10 FPS")



"""
FUNCTIONS
"""

def draw_playing_grid():
    """
    output: (None) draws rectangle of playing grid
    """
    #pygame.draw.rect(WINDOW,DARK_GREEN,[100,80,700,700])
    WINDOW.blit(pygame.transform.rotate(background,90), (100,80))

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

    elif button == "opt":
        # draw rect
        pygame.draw.rect(WINDOW,color,[100,20,200,50])
        # add "option" to opt button     
        WINDOW.blit(BTN_OPT , (100+40,20+10))

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
    elif button == "opt":
        return 100 <= mouse_x <= 300 and 20 <= mouse_y <= 70


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
    pygame.draw.rect(WINDOW,NICE_GREEN,[WINDOW_WIDTH/2-60+80,30,100,50])
    score_text = BTN_FONT.render(f'Score: {score}', True, BLACK)
    WINDOW.blit(score_text, (WINDOW_WIDTH/2-60,40))

def show_best_score(sscore):
    """
    input: score: (int) the current score
    output: (None) show the current score
    """
    pygame.draw.rect(WINDOW,NICE_GREEN,[WINDOW_WIDTH/2-60+360,30,100,50])
    best_score_text = BTN_FONT.render(f'Best score: {sscore}', True, BLACK)    
    WINDOW.blit(best_score_text, (WINDOW_WIDTH/2-60+180,40))
    


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
    if apple_coords in snake.coords or apple_coords in [bomb.coords for bomb in bombs] or apple_coords == golden_apple.coords:
        return generate_apple_coords()
    else:
        return apple_coords



def generate_golden_apple_coords():
    """
    output (tuple of (int, int)) : random point on grid for apple
    """
    gapple_coords = generate_random_coords()
    if gapple_coords in snake.coords or gapple_coords in [bomb.coords for bomb in bombs] or gapple_coords == apple.coords:
        return generate_golden_apple_coords()
    else:
        return gapple_coords



def generate_bomb_coords():
    """
    output (tuple of (int, int)) : random point on grid for bomb
    """
    bomb_coords = generate_random_coords()
    if bomb_coords in snake.coords or bomb_coords == apple.coords or bomb_coords in [bomb.coords for bomb in bombs] or bomb_coords == golden_apple.coords:
        return generate_bomb_coords()
    else:
        return bomb_coords



def init_best_score():
    if path.exists('best_score.txt.dat'):
        d = shelve.open('best_score.txt')
        best_score = d['score']
        best_score_face = d['score_face']
    else:
        d = shelve.open('best_score.txt')
        d['score'] = 0
        d['score_face'] = 0
        best_score = 0
        best_score_face = 0
    d.close()
    return (best_score, best_score_face)
            

       
def emotion_detection(thread_running):
    global current_mode, predicted_emotion
    # captures video feed
    cap = cv2.VideoCapture(0)
    while thread_running.is_set():
        if current_mode == "face":
            # captures each frame and returns boolean value and captured image
            ret, test_img = cap.read()
            if not ret:
                continue
            # get the gray representation of the frame
            gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)#GRAY)
            # uses the cascade classifier "face_haar_cascade" to detect the face(s)
            faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)
            # for each face detected
            for (x,y,w,h) in faces_detected:
                # draw a rectangle around the face
                cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=7)
                # crop Region Of Interest (face area from image)
                roi_gray = gray_img[y:y+w,x:x+h]
                # resize the image to 48*48
                roi_gray = cv2.resize(roi_gray,(48,48))
                # creates an array values between 0 and 255 (black and white)
                img_pixels = image.img_to_array(roi_gray).astype("uint8")

                # IMPORTANT:
                # img_pixels is an array of (48,48,3) of dtype uint8 

                # get the emotion with the highest rank
                with session.as_default():
                    with session.graph.as_default():
                        try:
                            # "neutral", "happy", "suprised" work :) 
                            predicted_emotion, score = detector.top_emotion(img_pixels)#emotions[max_index]
                            # print(predicted_emotion)
                            # put the emotion on top of the rectangle
                            cv2.putText(test_img, str(predicted_emotion), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                            # print("SUCCESS")
                        except:
                            #print("FAILED")
                            pass

            # resize the image to 500*350
            resized_img = cv2.resize(test_img, (500, 350))
            # show the image
            cv2.imshow('Facial emotion analysis ',resized_img)

            # wait until 'q' key is pressed (on the cv2 window)
            if cv2.waitKey(10) == ord('q'):
                break

    # stop the capture of video feed and destroys all cv2 windows
    cap.release()
    cv2.destroyAllWindows





"""
OTHER INITS
"""

# init bombs
bombs = []

apple = Apple((0,0), apple_image)
golden_apple = GoldenApple((0,0), golden_apple_image)

# init snake
snake = Snake([(420,400),(400,400)],20,0)
#               head      tail      x  y (init direction)

# init apple
apple = Apple(generate_apple_coords(), apple_image)

# init golden apple
golden_apple = GoldenApple(generate_golden_apple_coords(), golden_apple_image)

# eti
# init best_score
best_score, best_score_face = init_best_score()

# facial emotion detector
detector = FER(mtcnn=True)

face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# thread to run the emotion recognizer
thread_running = threading.Event()
thread_running.set()
th = threading.Thread(target = emotion_detection, args = (thread_running, ))
th.start()



bomb_count = 0

can_show_golden_apple = False

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

        if not snake_can_move:
            bomb_chkbox.update_checkbox(event)
            medium_speed_chkbox.update_checkbox(event)

        # mouse clicked
        if event.type == pygame.MOUSEBUTTONDOWN:

            # if quit button is clicked: exit game
            if mouse_hover_over_btn("quit", mouse_x, mouse_y):
                thread_running.clear()
                pygame.quit()
                sys.exit()

            # if optn button is clicked: open option window
            if mouse_hover_over_btn("opt", mouse_x, mouse_y):
                # opt_menu = OptionMenu(90)
                # opt_menu.launch()
                pass

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
                    FPS = 5
                else:
                    # change to classic
                    current_mode = "classic"
                    FPS = 15

                # increment m_count
                m_count += 1

        if current_mode == "classic":
            # key pressed
            if event.type == pygame.KEYDOWN and snake_can_move:
                # want to change directio so add 1 (if it passes 1 then change_direction is disabled)
                nb_desired_changes += 1
                if nb_desired_changes == 1:
                    snake.change_direction_with_keys(event)
    if current_mode == "face":
        if snake_can_move:
            snake.change_direction_with_emotion()
            

  
    # get mouse position coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # be able to change shade of button when hovering over it
    for button in buttons:
        change_btn_shade_on_hover(button, mouse_x, mouse_y)

    # draw grid
    draw_playing_grid()

    # show score
    show_score(score)

    # draw snake and apple and bombs

    bomb_chkbox.render_checkbox()
    if bomb_chkbox.is_unchecked():
        bombs = []
    else:
        for bomb in bombs:
            bomb.show()

    medium_speed_chkbox.render_checkbox()
    if medium_speed_chkbox.is_checked():
        FPS = 10

    if snake_can_move:
        bomb_count += 1
        if bomb_count % 100 == 0:
            bombs.append(Bomb(generate_bomb_coords(), bomb_image))

        # spawn golden apple
        if bomb_count % 500 == 0:
            golden_apple_count = 0
            can_show_golden_apple = True

        if can_show_golden_apple:
            golden_apple.show()
            golden_apple_count += 1
            if golden_apple_count % 100 == 0:
                del golden_apple
                can_show_golden_apple = False
                golden_apple = GoldenApple(generate_golden_apple_coords(), golden_apple_image)

    # show best_score
    if current_mode == "classic": 
        show_best_score(best_score)
    else:
        show_best_score(best_score_face)
    snake.show()
    apple.show()

    # check if snake can move (i.e. when "play" is pressed)
    if snake_can_move:
        snake.move()

    # snake dies
    if snake.died():

        # reset bombs
        bombs = []

        # reset snake
        del snake
        snake = Snake([(420,400),(400,400)],20,0)
        snake_can_move = False

        # reset apple
        del apple
        apple = Apple(generate_apple_coords(), apple_image)

        del golden_apple
        golden_apple = GoldenApple(generate_golden_apple_coords(), golden_apple_image)

        # Write best_score inside a file
        try:
            if current_mode == "classic":
                if score >= best_score:
                    d = shelve.open('best_score.txt')
                    d['score'] = score
                    d.close()
            elif current_mode == "face":
                if score >= best_score_face:
                    d = shelve.open('best_score.txt')
                    d['score_face'] = score
                    d.close()

        except:
            # print("BLIBLI")
            pass
        # reinit score
        score = 0
        # reinit best_score
        best_score, best_score_face = init_best_score()

            

 



    # update the game frames
    pygame.display.update()

    # we create a limitation so that the computer will not 
    # execute the game loop as many times as it can within a second. 
    FramePerSec.tick(FPS)