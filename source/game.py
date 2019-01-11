import sys
import time
import pygame
import thread
#begin programming the game

touchingGround = False
jumpIntervals = [4,4,3,3,3,2,2,2,2,1,1,1,-1,-1,-1,-2,-2,-2,-2,-3,-3,-3,-4,-4]

playerX = 0
playerY = 0

def jump:
    if(touchingGround == False):
        continue()
    if(touchingGround == True):
        for(i in jumpIntervals):
            playerY += i
            time.sleep(20)
    return

def initScreen():
    pygame.init()
    screen = pygame.display.set_mode((800,400))
    return

def mainGame():
    for event in pygame.event.get():
        if(event.Type == KEYUP):
            thread.start_new_thread(jump)
    return