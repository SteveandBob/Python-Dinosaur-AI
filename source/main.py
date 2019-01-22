#!/usr/bin/env python3
import pygame
import sys
import threading
import builtins

pygame.init()
scoreFont = pygame.font.SysFont('Times New Roman', 14)
screen = pygame.display.set_mode((1000, 300))
groundHeight = 210
currentScore = 0
builtins.score = currentScore
delay = 100

class enemy:
    def __init__(self, beginPos):
        self.xPos = beginPos
        self.cacti = pygame.image.load("./cacti.png")
        self.cactiRect = self.cacti.get_rect()
        self.height = self.cactiRect.bottom - self.cactiRect.top
        self.cactiRect = self.cactiRect.move([beginPos, groundHeight])
        self.speed = 10
        # the position the enemy begins at
        # when this block is spawned determines the position of the enemy

    def update(self):
        self.xPos -= self.speed
        self.cactiRect = self.cactiRect.move([-self.speed, 0])
        if self.xPos <= 0:
            self.cactiRect = self.cactiRect.move([1000 - self.xPos, 0])
            self.xPos = 1000
        screen.blit(self.cacti, self.cactiRect)
        # pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, (groundHeight + self.height), self.height, self.height))

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
        if enemy.cactiRect.top <= self.dinoRect.bottom - 20 and enemy.cactiRect.left <= self.dinoRect.right - 12:
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
        # pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, self.yPos, self.width, self.height))

def scoreCounter(block1, block2, delay):
    global currentScore
    delay = 100
    block1.speed = 10
    block2.speed = 10
    while(True):
        # error is in this part: "Text has zero width"
        currentScore += 1
        if currentScore <= 1000:
            if currentScore % 100 == 0:
                delay -= 10
                block1.speed += 1
                block2.speed += 1
        else:
            if currentScore % 100 == 0:
                delay -= 5
                if delay < 5:
                    delay = 5
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
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #done = True
                #continue
            #if player.grounded and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #player.jump()
        if(ai.finalOutput == 1):
            player.jump()
        for i in blocks:
            i.update()
        player.update(blocks)
        scoreText = scoreFont.render(str(currentScore), False, (0, 0, 0))
        screen.blit(scoreText, (1, 1))
        print(str(currentScore) + " " + str(blocks[0].speed) + " " + str(blocks[1].speed))
        pygame.display.flip()
        # this updates graphics, pygame is buffered and switches around buffers
        pygame.time.wait(40)
        # this limits game to 50 updates/sec


if __name__ == "__main__":
    main()
    pygame.time.wait(10)
    pygame.display.quit()
    sys.exit()
