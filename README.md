# py_snake_FER
Classic snake game developed in Python. Movement of snake controlled by either the keypad or by FER (Facial Emotion Recognition). 

## Execution
1. Create Python 3.8 environment. (Using pyenv or anaconda).
2. Inside the created Python environment, install necessary packages in **requirements.txt** with (`pip install -r requirements.txt`).
3. Run `python main_alt.py` to play.

## How to play
### Change from "face" mode to "classic" mode and vice-versa
While not playing, press "M : Classic" or "M : Face" to change from one mode to the other
### Mode "classic"
You can press "play" and use the keyboard's arrows to move the snake.
### Mode "face"
Be happy to turn left. Be surprised to turn right.
### Quit the game
Press "quit"

## Objects in game
 - 🍎 <b>Apple</b>: eat apples to earn 1 point. Every time you eat an Apple, a new one appears.
 - 🟡 🍎 <b>Golden Apple</b>: appears rarely and for short periods of time. Eat golden apples to earn 5 points.
 - 💣 <b>Bomb</b>: If this option is selected, bombs will gradually appear on the field. Hit a bomb and you die.


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
main_alt.py
```
