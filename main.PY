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
begin_sound = pygame.mixer.Sound('Resources/3,2,1 GO GO GO.wav')
pygame.mixer.music.load("Resources/background_music.mp3")
click_sound = pygame.mixer.Sound('Resources/clicking sound.wav')
click_sound.set_volume(1)
pygame.mixer.music.play(-1)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("Resources/Background.png")
imgGameOver = cv2.imread("Resources/GameOver.png")
imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/Bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/Bat2.png", cv2.IMREAD_UNCHANGED)
imgMenu = cv2.imread("Resources/main menu.png")
imgRules = cv2.imread("Resources/how to play.png")

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [300, 300]
speedX = 25
speedY = 25
gameOver = False
score = [0, 0]
rotation_angle = 0

# Menu states
state = "menu"  # Start with the menu

# Button areas 
play_button = (400, 183, 730, 285)
rules_button = (507, 355, 844, 457)
exit_button = (615, 535, 945, 646)
back_button = (1032, 591, 1240, 673)  # Back button on rules screen
game_over_back_button = (986, 585, 1240, 678)  # Back to menu button on Game Over screen

# Function to check if a click is inside a button box
def is_inside_box(py1, py2, box):
    x1_box, y1_box, x2_box, y2_box = box  # Renamed variables to avoid shadowing
    return x1_box <= py1 <= x2_box and y1_box <= py2 <= y2_box

# Function to rotate an image with an alpha channel
def rotate_image(image, angle):
    high, width, _ = image.shape
    center = (width // 2, high // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image[:, :, :3], rotation_matrix, (width, high), flags=cv2.INTER_LINEAR)
    alpha_channel = cv2.warpAffine(image[:, :, 3], rotation_matrix, (width, high), flags=cv2.INTER_LINEAR)
    rotated_image = cv2.merge((rotated_image, alpha_channel))
    return rotated_image

# Countdown variables
countdown_start_time = time.time()
countdown_finished = False

# Function to start the countdown
def start_countdown():
    global countdown_start_time, countdown_finished
    countdown_start_time = time.time()
    countdown_finished = False
    pygame.mixer.Sound.play(begin_sound)
    

# Main game loop
while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    if state == "menu":
        # Display the menu
        img = imgMenu.copy()
        cv2.imshow("Image", img)

        # Mouse click detection
        def mouse_click(event, mx, my, _, __):
            global state,gameOver,score,ballPos,speedX,speedY,rotation_angle,countdown_finished
            if event == cv2.EVENT_LBUTTONDOWN:
                if is_inside_box(mx, my, play_button):
                    pygame.mixer.Sound.play(click_sound)
                    gameOver = False
                    score = [0, 0]
                    countdown_finished = False
                    state = "play"
                    start_countdown()
                elif is_inside_box(mx, my, rules_button):
                    pygame.mixer.Sound.play(click_sound)
                    state = "rules"
                elif is_inside_box(mx, my, exit_button):
                    pygame.mixer.quit()
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

        cv2.setMouseCallback("Image", mouse_click)
        key = cv2.waitKey(1)
        if key == ord('q'):  # Quit using 'q'
            break

    elif state == "rules":
        # Display the rules screen
        img = imgRules.copy()
        cv2.imshow("Image", img)

        # Mouse click detection
        def mouse_click(event, mx, my, _, __):
            global state
            if event == cv2.EVENT_LBUTTONDOWN:
                if is_inside_box(mx, my, back_button):
                    pygame.mixer.Sound.play(click_sound)
                    state = "menu"

        cv2.setMouseCallback("Image", mouse_click)
        key = cv2.waitKey(1)
        if key == ord('q'):  # Quit using 'q'
            break

    elif state == "play":
        # Original game logic
        imgRaw = img.copy()
        hands, img = detector.findHands(img, flipType=False)  # With draw
        img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

        # Countdown logic
        if not countdown_finished:
            time_elapsed = time.time() - countdown_start_time
            countdown_value = 3 - int(time_elapsed)
            if countdown_value > 0:
                cv2.putText(img, str(countdown_value), (590, 330), cv2.FONT_HERSHEY_COMPLEX, 5, (92, 94, 255), 10)
            else:
                countdown_finished = True
            cv2.imshow("Image", img)
            key = cv2.waitKey(1)
            continue

        # Ball and game logic
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

        # Scoring and Game Over logic
        if ballPos[0] < 40:
            score[1] += 1
            ballPos = [400, 250]
            pygame.mixer.Sound.play(score_sound)
            speedX = -speedX
        if ballPos[0] > 1200:
            score[0] += 1
            ballPos = [800, 250]
            speedX = -speedX
            pygame.mixer.Sound.play(score_sound)

        if score[0] >= 5 or score[1] >= 5:
            gameOver = True

        if gameOver:
            imgGameOver = cv2.imread("Resources/gameOver.png")
            img = imgGameOver.copy()
            cv2.putText(img, f'{score[0]}-{score[1]}', (556, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (0, 0, 255), 5)
            
            # Add "Back to Main Menu" button logic
            def mouse_click(event, mx, my, _, __):
                global state
                if event == cv2.EVENT_LBUTTONDOWN:
                    if is_inside_box(mx, my , game_over_back_button):
                        pygame.mixer.Sound.play(click_sound)
                        state = "menu"

            cv2.setMouseCallback("Image", mouse_click)
        else:
            if ballPos[1] >= 500 or ballPos[1] <= 10:
                speedY = -speedY

            ballPos[0] += speedX
            ballPos[1] += speedY
            rotated_ball = rotate_image(imgBall, rotation_angle)
            img = cvzone.overlayPNG(img, rotated_ball, ballPos)
            cv2.putText(img, str(score[0]), (302, 665), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
            cv2.putText(img, str(score[1]), (902, 665), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

        img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))
        cv2.imshow("Image", img)

        key = cv2.waitKey(1)
        if key == ord('r'):  # Reset game
            pygame.mixer.Sound.play(restart_sound)
            countdown_finished = False
            start_countdown()
            speedX = speedX
            ballPos = [800, 250]
            gameOver = False
            score = [0, 0]
            imgGameOver = cv2.imread("Resources/GameOver.png")
        elif key == ord('q'):  # Quit
            break

pygame.mixer.quit()
cap.release()
cv2.destroyAllWindows()
