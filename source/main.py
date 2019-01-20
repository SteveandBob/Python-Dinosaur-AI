#!/usr/bin/env python3
import pygame
import sys
import os

pygame.init()
screen = pygame.display.set_mode((600, 300))
groundHeight = 210

class enemy:

    def __init__(self, beginPos):
        self.xPos = beginPos
        self.cacti = pygame.image.load("cacti.jpg")
        self.cactiRect = self.cacti.get_rect()
        self.height = self.cactiRect.bottom - self.cactiRect.top
        self.cactiRect = self.cactiRect.move([beginPos, groundHeight])
        # the position the enemy begins at
        # when this block is spawned determines the position of the enemy

    def update(self):
        self.xPos -= 13
        self.cactiRect = self.cactiRect.move([-13, 0])
        if self.xPos <= 0:
            self.cactiRect = self.cactiRect.move([600 - self.xPos, 0])
            self.xPos = 600
        screen.blit(self.cacti, self.cactiRect)
        #pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, (groundHeight + self.height), self.height, self.height))

class controller:

    def __init__(self):
        self.yPos = groundHeight
        self.xPos = 50
        self.dino = pygame.image.load("dinosaur.jpg")
        self.dinoRect = self.dino.get_rect()
        self.dinoRect = self.dinoRect.move([50, groundHeight])
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
        # TODO: noah you said that when cactis are added pygame can calcuate collisions
        # pls implement that here lol thnx
        if enemy.cactiRect.top <= self.dinoRect.bottom and enemy.cactiRect.left <= self.dinoRect.right:
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
            self.dinoRect = self.dinoRect.move([0, -self.jumpIncrement])
            self.jumpIncrement -= 2
        if self.yPos >= 200:
            self.grounded = True
            self.dinoRect.move([0, 200 - self.yPos])
            self.yPos = 200
        if self.collisionDetect(blocklist):
            pygame.quit()
            sys.exit()
        screen.blit(self.dino, self.dinoRect)
        #pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, self.yPos, self.width, self.height))

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
