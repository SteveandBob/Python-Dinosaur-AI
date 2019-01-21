#!/usr/bin/env python3
import pygame
import sys
import threading

pygame.init()
scoreFont = pygame.font.SysFont('Times New Roman', 14)
screen = pygame.display.set_mode((1000, 300))
groundHeight = 210
currentScore = 0
delay = 100

class enemy:
    def __init__(self, beginPos):
        self.xPos = beginPos
        self.cacti = pygame.image.load("./cacti.png")
        self.cactiRect = self.cacti.get_rect()
        self.height = self.cactiRect.bottom - self.cactiRect.top
        self.cactiRect = self.cactiRect.move([beginPos, groundHeight])
        # the position the enemy begins at
        # when this block is spawned determines the position of the enemy

    def update(self):
        self.xPos -= 13
        self.cactiRect = self.cactiRect.move([-13, 0])
        if self.xPos <= 0:
            self.cactiRect = self.cactiRect.move([1000 - self.xPos, 0])
            self.xPos = 1000
        screen.blit(self.cacti, self.cactiRect)
        #pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, (groundHeight + self.height), self.height, self.height))

class controller:
    def __init__(self):
        self.yPos = groundHeight
        self.xPos = 50
        self.dino = pygame.image.load("./dinosaur.png")
        self.dinoRect = self.dino.get_rect()
        self.dinoRect = self.dinoRect.move([50, groundHeight])
        self.width = 45
        self.height = 70
        self.grounded = True
        self.jumpIncrement = 0

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
        # pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, self.yPos, self.width, self.height))
        if self.collisionDetect(blocklist):
            pygame.quit()
            sys.exit()
        screen.blit(self.dino, self.dinoRect)
        #pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, self.yPos, self.width, self.height))

def scoreCounter(block1, block2, delay):
    global currentScore
    while(True):
        #error is in this part: "Text has zero width"
        currentScore += 1
        if(currentScore <= 100):
            delay = 100
            block1.speed = 1
            block2.speed = 1
        elif(currentScore <= 200):
            delay = 90
            block1.speed = 2
            block2.speed = 2
        elif(currentScore <= 300):
            delay = 80
            block1.speed = 3
            block2.speed = 3
        elif(currentScore <= 400):
            delay = 70
            block1.speed = 4
            block2.speed = 4
        elif(currentScore <= 500):
            delay = 60
            block1.speed = 5
            block2.speed = 5
        elif(currentScore <= 600):
            delay = 50
            block1.speed = 6
            block2.speed = 6
        elif(currentScore <= 700):
            delay = 40
            block1.speed = 7
            block2.speed = 7
        elif(currentScore <= 800):
            delay = 30
            block1.speed = 8
            block2.speed = 8
        elif(currentScore <= 900):
            delay = 20
            block1.speed = 9
            block2.speed = 9
        elif(currentScore <= 1000):
            delay = 10
            block1.speed = 10
            block2.speed = 10
        elif(currentScore > 1500):
            delay = 5
            block1.speed = 13
            block2.speed = 13
        elif(currentScore > 2500):
            delay = 1
            block1.speed = 15
            block2.speed = 15
        pygame.time.wait(delay)

block1 = enemy(1000)
block2 = enemy(1500)
blocks = [block1, block2]
player = controller()

class scoreThread(threading.Thread):
    def __init__(self, Name, ID):
        threading.Thread.__init__(self)
        self.Name = Name
        self.ID = ID
    def run(self):
        scoreCounter(block1, block2, delay)

def main():
    done = False
    score = scoreThread("thread1", 1)
    score.start()
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
        scoreText = scoreFont.render(str(currentScore), False, (0, 0, 0))
        screen.blit(scoreText, (1, 1))
        print (currentScore)
        pygame.display.flip()
        # this updates graphics, pygame is buffered and switches around buffers
        pygame.time.wait(25)
        # this limits game to 50 updates/sec

if __name__ == "__main__":
    main()
    pygame.time.wait(10)
    pygame.display.quit()
