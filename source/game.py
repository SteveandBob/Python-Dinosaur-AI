import sys
import time
import pygame
import thread
#begin programming the game

touchingGround = False
jumpIntervals = [4,4,3,3,3,2,2,2,2,1,1,1,-1,-1,-1,-2,-2,-2,-2,-3,-3,-3,-4,-4]

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
obstacle1
obstacle2
obstacle3

class obstacle:
    def __init__(self, uniqueID):
        self.ID = uniqueID
    def getID(self):
        return self.ID
    def draw(self):
        pygame.draw.rect(screen, BLACK, [initX, initY, initX + blockW, initY + blockH])
    def move(self):
        initX -= 5

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
    if(not obstacle1):
        obstacle1 = obstacle(1)
    elif(not obstacle2):
        obstacle2 = obstacle(2)
    elif(not obstacle3):
        obstacle3 = obstacle(3)
    return
