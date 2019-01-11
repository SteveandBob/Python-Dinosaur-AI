import sys
import time
import pygame
#begin programming the game

touchingGround = False
jumpIntervals = [4,4,3,3,3,2,2,2,2,1,1,1,-1,-1,-1,-2,-2,-2,-2,-3,-3,-3,-4,-4]

playerX = 0
playerY = 0

def jump:
    if(touchingGround == False):
        continue()
    if(touchingGround == True):
        for(int i = 0, i < len(jumpIntervals), ++i):
            playerY += jumpIntervals[i]
    return

def initScreen():
    pygame.init()
    screen = pygame.display.set_mode((800,400))
    return

def mainGame():
    for event in pygame.event.get():
        if(event.Type == KEYUP):
            jump()
    return