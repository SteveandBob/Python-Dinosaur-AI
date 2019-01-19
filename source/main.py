#!/usr/bin/env python3
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 300))
groundHeight = 210

class enemy:

    def __init__(self, beginPos):
        self.xPos = beginPos
        self.height = 30
        # the position the enemy begins at
        # when this block is spawned determines the position of the enemy

    def update(self):
        self.xPos -= 13
        if self.xPos <= 0:
            self.xPos = 600
        pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, (groundHeight + self.height), self.height, self.height))

currentScore = 0

def scoreCounter:
    def __init__(self, threadName):
        self.threadName = threadName
        self.delay = 100
    def run(self, player):
        while(player.collisionDetect == False):
            currentScore += 1
            pygame.time.wait(self.delay)
            if(currentScore <= 100):
                self.delay = 100
            elif(currentScore <= 200):
                self.delay = 90
            elif(currentScore <= 300):
                self.delay = 80
            elif(currentScore <= 400):
                self.delay = 70
            elif(currentScore <= 500):
                self.delay = 60
            elif(currentScore <= 600):
                self.delay = 50
            elif(currentScore <= 700):
                self.delay = 40
            elif(currentScore <= 800):
                self.delay = 30
            elif(currentScore <= 900):
                self.delay = 20
            elif(currentScore <= 1000):
                self.delay = 10
            elif(currentScore > 1500):
                self.delay = 5
            elif(currentScore > 2500):
                self.delay = 1

class controller:

    def __init__(self):
        self.yPos = groundHeight
        self.xPos = 50
        self.width = 45
        self.height = 70
        self.grounded = True
        self.jumpIncrement = 20

    def jump(self):
        # sets up player to jump
        # jump is updated in the update() function
        if self.yPos == 200 and self.grounded:
            self.grounded = False
            self.jumpIncrement = 20

    def isTouching(self, enemy):
        # TODO: noah you said that when sprites are added pygame can calcuate collisions
        # pls implement that here lol thnx
        if enemy.xPos > self.xPos and enemy.xPos <= (self.xPos + self.width - 5):
            if (self.yPos + self.height) >= (enemy.height + groundHeight):
                print("true")
                return True
        return False

    def collisionDetect(self, enemy):
        for i in enemy:
            if self.isTouching(i):
                return True
        return False

    def update(self, blocklist):
        # updates the player and draws it
        # also handles jump after it has been initiated
        if not self.grounded:
            self.yPos -= self.jumpIncrement
            self.jumpIncrement -= 2
        if self.yPos >= 200:
            self.grounded = True
            self.yPos = 200
        if self.collisionDetect(blocklist):
            pygame.quit()
            sys.exit()
        pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, self.yPos, self.width, self.height))

def main():
    done = False
    block1 = enemy(600)
    block2 = enemy(900)
    blocks = [block1, block2]
    player = controller()
    while not done:
        screen.fill((245, 245, 245))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                continue
            if player.grounded and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.jump()

        for i in blocks:
            i.update()
        player.update(blocks)

        pygame.display.flip()
        # this updates graphics, pygame is buffered and switches around buffers
        pygame.time.wait(50)
        # this limits game to 25 updates/sec


if __name__ == "__main__":
    main()
    pygame.time.wait(10)
