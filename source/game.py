#!/usr/bin/env python3
# shebang for linux/mac/unix users

import sys
import pygame
import threading
import random

# begin programming the game
spawn1 = False
spawn2 = False
speed = 5
screenY = 400
screenX = 800
minTime = 500
maxTime = 2000
delay = 0

pygame.init()
screen = pygame.display.set_mode((screenX, screenY))


def refreshScreen():
    screen.fill((255, 255, 255))
    return


class controller:
    # I have no clue what to name it, I want the instance to be named
    # player, while the class be named controller

    # player variables:

    # player pos:
    playerX = 100
    playerY = 350

    # player dimensions:
    width = 20
    height = 40

    # player attributes:
    touchingGround = True

    # player jump intervals
    jumpIntervals = [10, 10, 6, 6, 6, 3, 3, 3, 3, 2, 2, 1]
    for i in range(12):
        jumpIntervals.append(jumpIntervals[11 - i] * -1)

    def getXpos(self):
        return self.playerX

    def getXWidth(self):
        return self.playerX + self.width

    def getYpos(self):
        return self.playerY

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), [self.playerX, self.playerY, self.playerX + self.width, self.playerY + self.height])

    def jump(self, threadName, delay):
        if(self.touchingGround):
            for i in self.jumpIntervals:
                self.playerY += i
                pygame.draw.rect(screen, (255, 0, 0), [self.playerX, self.playerY, self.playerX + self.width, self.playerY + self.height])
                pygame.time.wait(delay)
                if(exitFlag):
                    threadName.exit()
        return

    def isGrounded(self):
        return self.touchingGround

    def isTouching(self, enemy):
        if (((self.playerX + self.width) > enemy.getXpos()) and ((self.playerX + self.width) < enemy.getXWidth()) and (self.playerY < enemy.getYHeight()) and (self.playerX > enemy.getXpos()) and (self.playerX < enemy.getXWidth())):
            # TODO: Make if statement less cancer
            return True
        if (self.playerY <= (screenY - 50)):
            self.playerY = screenY - 50
            self.touchingGround = True
        else:
            self.touchingGround = False
        return False
        # if(((self.playerX + self.width) > (block1X or block2X)) and ((self.playerX + self.width) < ((block1X + blockW) or (block2X + blockW))) and (self.playerY < (initY - blockH)) and ((self.playerX > (block1X or block2X))) and (self.playerX < ((block1X + blockW) or (block2X + blockW)))):
        #     # TODO: a feeble attempt at making this less cancer?
        #     pygame.quit()
        #     sys.exit()
        # if(self.playerY <= 350):
        #     self.playerY = 350
        #     self.touchingGround = True
        # else:
        #     self.touchingGround = False


class enemy:
    # the class is called enemy, the individual instances itself are called block1 and block2
    # so that syntax change isn't huge

    # x position of block
    blockX = 0

    # dimensions of block
    blockW = 25
    blockH = 45

    # initial spawn position of block
    initX = 900
    initY = 350

    def __init__(self, beginpos):
        self.blockX = beginpos

    def getXpos(self):
        return self.blockX

    def getXWidth(self):
        return self.blockX + self.blockW

    def getYHeight(self):
        return self.initY - self.blockH

    def moveBlock(self):
        self.blockX -= speed
        pygame.draw.rect(screen, (0, 0, 0), [self.blockX, self.initY, self.initX + self.blockW, self.initY + self.blockH])
        if(self.blockX <= -50):
            delay = random.randint(minTime, maxTime)
            pygame.time.wait(delay)
            self.blockX = 900


exitFlag = 0


def mainGame():

    player = controller()

    block1 = enemy(900)
    block2 = enemy(1400)

    class jumpThreads(threading.Thread):

        def __init__(self, threadID, name):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name

        def run(self):
            player.jump(self.name, 20)

    jumpThread = jumpThreads(1, "jumping")

    def moveBlocks():
        block1.moveBlock()
        block2.moveBlock()

    def updateScreen():
        player.draw()

    def collisionDetect():
        if (player.isTouching(block1) or player.isTouching(block2)):
            pygame.quit()
            sys.exit()

    while(True):
        ai.ai.run()
        refreshScreen()
        for event in pygame.event.get():
            if(pygame.event.EventType == pygame.key.get_pressed()):
                if(pygame.event.key == pygame.K_UP):
                    if(not jumpThread.isAlive()):
                        jumpThread.start()
                    else:
                        jumpThread.join()
            elif(pygame.event.EventType == pygame.QUIT):
                pygame.quit()
                sys.exit()
        else:
            updateScreen()
        moveBlocks()
        collisionDetect()
        pygame.display.flip()
    return
