import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pygame
import time

# Initialize pygame mixer for sound effects
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("Resources/HIT SOUND.wav")
score_sound = pygame.mixer.Sound("Resources/SCORE SOUND.wav")
restart_sound = pygame.mixer.Sound('Resources/AGAIN.mp3')
begin_sound = pygame.mixer.Sound('Resources/3,2,1,GO GO GO.mp3')

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("Resources/Background.png")
imgGameOver = cv2.imread("Resources/gameOver.png")
imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/Bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/Bat2.png", cv2.IMREAD_UNCHANGED)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [300, 300]
speedX = 20
speedY = 20
gameOver = False
score = [0, 0]
rotation_angle = 0

# Countdown variables
countdown_start_time = None
countdown_finished = False

# Function to rotate an image with an alpha channel
def rotate_image(image, angle):
    height, width, _ = image.shape
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image[:, :, :3], rotation_matrix, (width, height), flags=cv2.INTER_LINEAR)
    alpha_channel = cv2.warpAffine(image[:, :, 3], rotation_matrix, (width, height), flags=cv2.INTER_LINEAR)
    rotated_image = cv2.merge((rotated_image, alpha_channel))
    return rotated_image


# Function to start the countdown
def start_countdown():
    global countdown_start_time
    countdown_start_time = time.time()  # Store the current time in countdown_start_time
    pygame.mixer.Sound.play(begin_sound)

# Start the countdown
start_countdown()

# Main game loop
while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    # Find hands and landmarks
    hands, img = detector.findHands(img, flipType=False)  # With draw

    # Overlay the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # Countdown logic
    if not countdown_finished:
        if countdown_start_time is not None:  # Ensure countdown_start_time is valid
            time_elapsed = time.time() - countdown_start_time
            countdown_value = 3 - int(time_elapsed)

            # Display the countdown
            if countdown_value > 0:
                cv2.putText(img, str(countdown_value), (600, 400), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 0, 255), 10)
            else:
                countdown_finished = True

        # Render bats during countdown
        if hands:
            for hand in hands:
                x, y, w, h = hand['bbox']
                h1, w1, _ = imgBat1.shape
                y1 = y - h1 // 2
                x1 = x - w1 // 2
                x1 = np.clip(x1, 29, 1280 - w1)
                y1 = np.clip(y1, 20, 415)

                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat1, (x1, y1))
                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat2, (x1, y1))

        # Display frame and continue
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('r'):  # Allow reset during countdown
            start_countdown()
            ballPos = [100, 100]
            score = [0, 0]
            gameOver = False
        continue


    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            x1 = x - w1 // 2
            x1 = np.clip(x1, 29, 1280 - w1)
            y1 = np.clip(y1, 20, 415)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (x1, y1))
                if x1 - 50 < ballPos[0] < x1 + w1 and y1 - 50 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    rotation_angle += 20
                    pygame.mixer.Sound.play(hit_sound)
            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (x1, y1))
                if x1 - 50 < ballPos[0] < x1 + w1 and y1 - 50 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    rotation_angle += 20
                    pygame.mixer.Sound.play(hit_sound)

    # Score and Game Over
    if ballPos[0] < 40:  # Player 2 scores
        score[1] += 1
        ballPos = [640, 360]
        pygame.mixer.Sound.play(score_sound)
    if ballPos[0] > 1200:  # Player 1 scores
        score[0] += 1
        ballPos = [640, 360]
        pygame.mixer.Sound.play(score_sound)

    if score[0] >= 5 or score[1] >= 5:  # Game ends at 5 points
        gameOver = True

    if gameOver:
        img = imgGameOver
        cv2.putText(img, f'{score[0]}-{score[1]}', (550, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (0, 0, 255), 5)
    else:
        # Move the Ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Rotate the ball
        rotated_ball = rotate_image(imgBall, rotation_angle)
        img = cvzone.overlayPNG(img, rotated_ball, ballPos)

        # Display the score
        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    # Small camera overlay
    img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))

    # Show the final image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):  # Reset game on pressing 'r'
        pygame.mixer.Sound.play(restart_sound)
        ballPos = [400, 400]
        speedX = 40
        speedY = 40
        gameOver = False
        score = [0, 0]
        rotation_angle = 0  # Reset rotation angle
        imgGameOver = cv2.imread("Resources/gameOver.png") # Rest the final score