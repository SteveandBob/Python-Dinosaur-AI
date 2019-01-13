#!/usr/bin/env python3
# shebang for linux/mac/unix users

import sys
import time
import pygame
import threading
import random

# begin programming the game

touchingGround = True
jumpIntervals = [10, 10, 6, 6, 6, 3, 3, 3, 3, 2, 2, 1, -1, -2, -2, -3, -3, -3, -3, -6, -6, -6, -10, -10]

spawn1 = False
spawn2 = False
playerX = 100
playerY = 350
initX = 1000
initY = 350
block1X = 900
block2X = 1400
blockW = 25
blockH = 45
width = 20
height = 40
speed = 5
screenY = 400
screenX = 800
minTime = 50
maxTime = 2000
delay = 0

pygame.init()
screen = pygame.display.set_mode((screenX, screenY))


def refreshScreen():
    screen.fill((255, 255, 255))
    return


def moveBlocks():
    # you forgot this
    global block1X, block2X
    # however, this is the wrong way of passing in global variables in python
    # what it should be instead is that we pass in the global variables
    # then, when we call it, we call `block1X = moveBlocks(block1X)`
    # and then call `block2X = moveBlocks(block2X)`
    # but, I am a lazy bastard, and hence I put `global block1X, block2X`
    # TODO #1 - FIX THIS LAZY SLOP OF A HACK
    # - ian
    block1X -= speed
    block2X -= speed
    pygame.draw.rect(screen, (0, 0, 0), [block1X, initY, initX + blockW, initY + blockH])
    pygame.draw.rect(screen, (0, 0, 0), [block2X, initY, initX + blockW, initY + blockH])
    if(block1X <= -50):
        delay = random.randint(minTime, maxTime)
        time.wait(delay)
        block1X = 900
    if(block2X <= -50):
        delay = random.randint(minTime, maxTime)
        time.wait(delay)
        block2X = 900


def drawPlayer():
    pygame.draw.rect(screen, (255, 0, 0), [playerX, playerY, playerX + width, playerY + height])
    return

exitFlag = 0

class jumpThreads(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        jump(self.name, 20)

def jump(threadName, delay):
    global playerY
    # TODO #2 - FIX STATEMENT ABOVE
    # SEE TODO #1
    # - ian
    if(touchingGround):
        for i in jumpIntervals:
            playerY += i
            pygame.draw.rect(screen, (255, 0, 0), [playerX, playerY, playerX + width, playerY + height])
            time.wait(delay)
            if(exitFlag):
                threadName.exit()
    return

jumpThread = jumpThreads(1, "jumping")

def collisionDetect():
    global playerY, touchingGround
    # TODO #3 - FIX STATEMENT ABOVE
    # SEE TODO #1
    # - ian
    if((playerX + width) > (block1X or block2X) and playerY < (initY + blockH) and playerX < (block1X or block2X)):
        pygame.quit()
        sys.exit()
    if(playerY <= 350):
        playerY = 350
        touchingGround = True
    else:
        touchingGround = False


def mainGame():
    while(True):
        refreshScreen()
        if(pygame.event.get()):
            if(pygame.event.EventType == pygame.key.get_pressed()):
                if(pygame.event.key == pygame.K_UP):
                    if(jumpThread.isAlive() == False):
                        jumpThread.start()
                    else:
                        jumpThread.join()
            elif(pygame.event.EventType == pygame.QUIT):
                pygame.quit()
                sys.exit()
        else:
            drawPlayer()
        moveBlocks()
        collisionDetect()
    return
