# py_snake_facial_expressions
Classic snake game developed in Python. Movement of snake controlled by facial expressions. 

## Execution
To currently execute the program and play the game, you must have the following packages :
- pygame
- os
- cv2
- numpy
- threading
- sys
- random
- shelve
- keras
- tensorflow

After verifying that you have all the required packages, please use the command :
```bash
python3 main.py
```

You can now play the game.

## How to play
### Change from "face" mode to "classic" mode and vice-versa
While not playing, press "M : Classic" or "M : Face" to change from one mode to the other
### Mode "classic"
You can press "play" and use the keyboard's arrows to move the snake.
### Mode "face"
Still in development (allows you to play snake with emotion recognition).
### Quit the game
Press "quit"


## Files
### Detection of facial emotions: 
```bash
fer.h5
fer.json
haarcascade_frontalface_default.xml
videoTester.py
```

### Best score:
```bash
best_score.txt.bak
best_score.txt.dat
best_score.txt.dir
```

### Main file:
```bash
main.py
```
