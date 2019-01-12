import sys
import time
import pygame
import threading
import random
from pygame import *
#begin programming the game

touchingGround = True
jumpIntervals = [10,10,6,6,6,3,3,3,3,2,2,1,-1,-2,-2,-3,-3,-3,-3,-6,-6,-6,-10,-10]

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
    screen.fill((255,255,255))
    return

def moveBlocks():
    block1X -= speed
    block2X -= speed
    pygame.draw.rect(screen, (0,0,0), [block1X, initY, initX + blockW, initY + blockH])
    pygame.draw.rect(screen, (0,0,0), [block2X, initY, initX + blockW, initY + blockH])
    if(block1X <= -50):
        delay = random.randint(minTime, maxTime)
        time.wait(delay)
        block1X = 900
    if(block2X <= -50):
        delay = random.randint(minTime, maxTime)
        time.wait(delay)
        block2X = 900

def drawPlayer():
    pygame.draw.rect(screen, (255,0,0), [playerX, playerY, playerX + width, playerY + height])
    return

def jump():
    if(touchingGround == True):
        for i in jumpIntervals:
            playerY += i
            pygame.draw.rect(screen, (255,0,0), [playerX, playerY, playerX + width, playerY + height])
            time.wait(20)
    return

def collisionDetect():
    if((playerX + width) > (blockX1 or blockX2) and playerY < (initY + blockH) and playerX < (blockX1 or blockX2)):
        quit()
    if(playerY <= 350):
        playerY = 350
        touchingGround = True
    else:
        touchingGround = False

def mainGame():
    while(True):
        refreshScreen()
        if(pygame.event.get()):
            if(event.type == pygame.key.get_pressed()):
                if(event.key == K_UP):
                    jump()
             elif(event.type == QUIT):
                pygame.quit()
                sys.exit()
        else:
            drawPlayer()
        moveBlocks()
        collisionDetect()
    return
