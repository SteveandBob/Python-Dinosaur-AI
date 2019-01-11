import sys
import time
import pygame
import thread
import random
#begin programming the game

touchingGround = False
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

def spawn(blockX):
    delay = round(random.uniform(minTime, maxTime), 1)
    time.sleep(delay)
    while(blockX > 0):
        pygame.draw.rect(screen, BLACK, [blockX, initY, initX + blockW, initY + blockH])
        blockX -= speed
        time.sleep(20)
    return

def drawPlayer():
    pygame.draw.rect(screen, RED, [playerX, playerY, playerX + width, playerY + height])
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
    return

def mainGame():
    for event in pygame.event.get():
        if(event.Type == KEYUP):
            thread.start_new_thread(jump)
    drawPlayer()
    thread.start_new_thread(spawn, (initX))
    thread.start_new_thread(spawn, (initX))
    return