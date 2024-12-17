# Ping Pong Game with Hand Tracking 🎮✋

A fun and interactive Ping Pong game built with Python, OpenCV, and CvZone! Control the paddles using real-time hand tracking, challenge a friend, and see who reaches 5 points first. 🚀

## Project Team
- Ahmed Mosaad
- Ahmed Shaheen
- Mohammed Helal
- Islam Mohammed 

## Features
- Real-time hand tracking for paddle control.
- Dynamic ball physics for an exciting experience.
- Score tracking and game-over screen.

## How to Play
1. Clone this repository:
git clone https://github.com/Mohammed-Helal/PingPongPY.git

2. Install dependencies:
pip install -r requirements.txt

3. Run the game:
python main.py

4. Use your left and right hands to control the paddles and bounce the ball.

## Assets
Place all required images in the `Resources/` folder:
- `Background.png`: The background of the game.
- `gameOver.png`: The game-over screen.
- `Ball.png`: The ball image.
- `bat1.png` and `bat2.png`: Paddle images for Player 1 and Player 2.

## Controlling Speed

You can control the speed of the object in the game by modifying the `speedX` and `speedY` variables in the code. These variables represent the movement speed of the object in the horizontal and vertical directions, respectively.

- **`speedX`**: Controls the speed of the object in the horizontal (X) direction.
- **`speedY`**: Controls the speed of the object in the vertical (Y) direction.

By changing the values of `speedX` and `speedY`, you can adjust the speed of the object's movement, allowing for customized gameplay.

Example:
```c
int speedX = 20;  // Speed in the horizontal direction
int speedY = 30;  // Speed in the vertical direction

## Controls
- Press `R` to restart the game.
- The first player to reach 5 points wins!

## Requirements
- Python 
- OpenCV
- CvZone
- NumPy


