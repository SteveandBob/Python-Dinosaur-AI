import sys
import time
import pygame
import thread
import random
from pygame import *
#begin programming the game

touchingGround = True
jumpIntervals = [10,10,6,6,6,3,3,3,3,2,2,1,-1,-2,-2,-3,-3,-3,-3,-6,-6,-6,-10,-10]

playerX = 100
playerY = 350
initX = 1000
initY = 350
blockW = 25
blockH = 45
width = 20
height = 40
speed = 5
screenY = 400
screenX = 800
minTime = 0.5
maxTime = 2
delay = 0
scoreDelay = 100

def spawn(blockX):
    delay = round(random.uniform(minTime, maxTime), 1)
    time.sleep(delay)
    while(blockX > 0):
        pygame.draw.rect(screen, (0,0,0), [blockX, initY, initX + blockW, initY + blockH])
        blockX -= speed
        time.sleep(20)
    return

def drawPlayer():
    pygame.draw.rect(screen, (255,0,0), [playerX, playerY, playerX + width, playerY + height])
    return

def jump():
    if(touchingGround == True):
        for i in jumpIntervals:
            playerY += i
            time.sleep(20)
    return

def initScreen():
    pygame.init()
    screen = pygame.display.set_mode((screenX, screenY))
    screen.fill((255,255,255))
    return

def collisionDetect():
    if((playerX + width) > blockX and playerY < (initY + blockH) and playerX < blockX):
        quit()
    if(playerY <= 350):
        playerY = 350
        touchingGround = True
    else:
        toughingGround = False

def mainGame():
    for EVENT in pygame.event.get():
        if(EVENT.Type == KEYDOWN):
            if(pygame.key.get_pressed()[K_UP]):
                thread.start_new_thread(jump)
        elif(EVENT.Type == QUIT()):
            quit()
    drawPlayer()
    thread.start_new_thread(spawn, (initX))
    thread.start_new_thread(spawn, (initX))
    collisionDetect()
    return