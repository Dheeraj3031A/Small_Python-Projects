import pygame
import random
import sys
import os
import time
from pygame.locals import *

# Constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5
count = 3

# Function to terminate the game
def terminate():
    pygame.quit()
    sys.exit()

# Function to wait for the player to press a key
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # escape quits
                    terminate()
                return

# Function to check if the player has hit a baddie
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

# Function to draw text on the screen
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Initialize pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Car Race')
pygame.mouse.set_visible(False)

# Fonts
font = pygame.font.SysFont(None, 30)

# Sounds
gameOverSound = pygame.mixer.Sound('music/crash.wav')
pygame.mixer.music.load('music/car.wav')
laugh = pygame.mixer.Sound('music/laugh.wav')

# Images
playerImage = pygame.image.load('images/car1.png')
car3 = pygame.image.load('images/car3.png')
car4 = pygame.image.load('images/car4.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('images/car2.png')
sample = [car3, car4, baddieImage]
wallLeft = pygame.image.load('images/left.png')
wallRight = pygame.image.load('images/right.png')

# Start screen
drawText('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
drawText('And Enjoy', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3) + 30)
pygame.display.update()
waitForPlayerToPressKey()
zero = 0

# Load or initialize topScore from file
if not os.path.exists("data/save.dat"):
    with open("data/save.dat", 'w') as f:
        f.write(str(zero))

with open("data/save.dat", 'r') as v:
    topScore = v.readline().strip()  # Remove leading/trailing whitespaces

# Check if topScore is empty, if so, set it to zero
if not topScore:
    topScore = '0'

# Main game loop
while count > 0:
    # Game initialization
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    # Game loop
    while True:
        # Increase score
        score += 1

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

        # Add new baddies
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = 30
            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(random.choice(sample), (23, 47)),
                         }
            baddies.append(newBaddie)
            sideLeft = {'rect': pygame.Rect(0, 0, 126, 600),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface': pygame.transform.scale(wallLeft, (126, 599)),
                        }
            baddies.append(sideLeft)
            sideRight = {'rect': pygame.Rect(497, 0, 303, 600),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(wallRight, (303, 599)),
                         }
            baddies.append(sideRight)

        # Move the player
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the baddies
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # Remove off-screen baddies
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world
        windowSurface.fill(BACKGROUNDCOLOR)
        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 128, 20)
        drawText('Rest Life: %s' % (count), font, windowSurface, 128, 40)
        windowSurface.blit(playerImage, playerRect)
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])
        pygame.display.update()

        # Check if the player has hit a baddie
        if playerHasHitBaddie(playerRect, baddies):
            if score > int(topScore):
                with open("data/save.dat", 'w') as g:
                    g.write(str(score))
                topScore = score
            break

        mainClock.tick(FPS)

    # Game Over screen
    pygame.mixer.music.stop()
    count -= 1
    gameOverSound.play()
    time.sleep(1)
    if count == 0:
        laugh.play()
        drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80,
                 (WINDOWHEIGHT / 3) + 30)
        pygame.display.update()
        time.sleep(2)
        waitForPlayerToPressKey()
        count = 3
        gameOverSound.stop()
