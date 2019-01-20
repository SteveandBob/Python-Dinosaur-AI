#!/usr/bin/env python3
import pygame
import sys
import threading

pygame.init()
scoreFont = pygame.font.SysFont('Times New Roman', 14)
screen = pygame.display.set_mode((1000, 300))
groundHeight = 210
currentScore = 0
scoreText = scoreFont.render(str(currentScore), False, (0, 0, 0))

class enemy:

    def __init__(self, beginPos):
        self.xPos = beginPos
        self.cacti = pygame.image.load("./cacti.jpg")
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

class scoreThread(threading.Thread):
    def __init__(self, Name, ID):
        threading.Thread.__init__(self)
        self.Name = Name
        self.ID = ID
    def run(self):
        scoreCounter()

def scoreCounter(self, player, block1, block2):
    while(not player.collisionDetect):
        currentScore += 1
        pygame.time.wait(self.delay)
        screen.blit(str(scoreText), (0, 0))
        if(currentScore <= 100):
            self.delay = 100
            block1.speed = 13
            block2.speed = 13
        elif(currentScore <= 200):
            self.delay = 90
            block1.speed = 14
            block2.speed = 14
        elif(currentScore <= 300):
            self.delay = 80
            block1.speed = 15
            block2.speed = 15
        elif(currentScore <= 400):
            self.delay = 70
            block1.speed = 16
            block2.speed = 16
        elif(currentScore <= 500):
            self.delay = 60
            block1.speed = 17
            block2.speed = 17
        elif(currentScore <= 600):
            self.delay = 50
            block1.speed = 18
            block2.speed = 18
        elif(currentScore <= 700):
            self.delay = 40
            block1.speed = 19
            block2.speed = 19
        elif(currentScore <= 800):
            self.delay = 30
            block1.speed = 20
            block2.speed = 20
        elif(currentScore <= 900):
            self.delay = 20
            block1.speed = 21
            block2.speed = 21
        elif(currentScore <= 1000):
            self.delay = 10
            block1.speed = 22
            block2.speed = 22
        elif(currentScore > 1500):
            self.delay = 5
            block1.speed = 25
            block2.speed = 25
        elif(currentScore > 2500):
            self.delay = 1
            block1.speed = 30
            block2.speed = 30

score = scoreThread("thread1", 1)

class controller:
    def __init__(self):
        self.yPos = groundHeight
        self.xPos = 50
        self.dino = pygame.image.load("./dinosaur.jpg")
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
            self.jumpIncrement = 15

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
        pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, self.yPos, self.width, self.height))
        if self.collisionDetect(blocklist):
            pygame.quit()
            sys.exit()
        screen.blit(self.dino, self.dinoRect)
        #pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, self.yPos, self.width, self.height))

def main():
    done = False
    block1 = enemy(1000)
    block2 = enemy(1500)
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
        screen.blit(scoreText, (0, 0))
        pygame.display.flip()
        # this updates graphics, pygame is buffered and switches around buffers
        pygame.time.wait(50)
        # this limits game to 25 updates/sec


if __name__ == "__main__":
    main()
    pygame.time.wait(10)
