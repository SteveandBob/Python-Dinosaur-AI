#!/usr/bin/env python3
import pygame
import sys
import threading
import random
import array

pygame.init()
pygame.mixer.quit()
scoreFont = pygame.font.SysFont('Times New Roman', 14)
screen = pygame.display.set_mode((1000, 300))
groundHeight = 210
currentScore = 0
delay = 100
openFile = open("weightValues.txt", "r+")

class enemy:
    global currentScore
    def __init__(self, beginPos):
        self.xPos = beginPos
        self.cacti = pygame.image.load("./cacti.png")
        self.cactiRect = self.cacti.get_rect()
        self.height = self.cactiRect.bottom - self.cactiRect.top
        self.cactiRect = self.cactiRect.move([beginPos, groundHeight])
        self.speed = 10
        self.minRandDist = 40
        self.maxRandDist = 150
        # the position the enemy begins at
        # when this block is spawned determines the position of the enemy

    def update(self):

        self.xPos -= self.speed
        self.cactiRect = self.cactiRect.move([-self.speed, 0])
        if self.xPos <= 0:
            self.randomDist = random.randint((self.speed * 10) + 0, (self.speed * 10) + 0)
            # TODO: NOTICE THE + 50 AND THE + 100 IN THE ABOVE LINE
            # WE CAN SHORTEN IT AS AI GETS GOOD
            # basically, the above line makes sure the dinosaur always has enough space to make the jump
            self.cactiRect = self.cactiRect.move([(1000 + self.randomDist) - self.xPos, 0])
            self.xPos = 1000 + self.randomDist
        screen.blit(self.cacti, self.cactiRect)
        if currentScore % 100 == 0:
            self.minRandDist += 20
            self.maxRandDist += 20
        # pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, (groundHeight + self.height), self.height, self.height))

class controller:
    def __init__(self):
        self.notDead = True
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
        if enemy.cactiRect.top <= self.dinoRect.bottom - 20 and enemy.cactiRect.left <= self.dinoRect.right - 12:
                print("true")
                return True
        return False

    def collisionDetect(self, enemy):
        global exitFlag
        for i in enemy:
            if self.isTouching(i):
                return True
        return False

    def update(self, blocklist):
        if self.notDead:
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
            screen.blit(self.dino, self.dinoRect)
            # pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, self.yPos, self.width, self.height))

    def delete(self):
        self.notDead = False

def scoreCounter(block1, block2, block3, playerList, delay):  # add a delay variable
    global currentScore
    currentScore = 0
    while(True):
        currentScore += 1
        if currentScore <= 1000:
            if currentScore % 100 == 0:
                delay -= 10
                block1.speed += 1
                block2.speed += 1
                block3.speed += 1
        else:
            if currentScore % 100 == 0:
                delay -= 5
                if delay < 5:
                    delay = 5
            if(playerList[0].notDead == False and playerList[1].notDead == False and playerList[2].notDead == False and playerList[3].notDead == False and playerList[4].notDead == False):
                 sys.exit()
            pygame.time.wait(delay)

class ai:
    def __init__(self):
        self.aiScore = 0
        self.notAlive = False
        self.quit = False
        self.playerSpeed = 0
        self.onGround = 1
        self.blockDist = 0
        self.nextBlockPos = 0
        self.modOut1 = 0
        self.modOut2 = 0
        self.modOut3 = 0
        self.finalOutput = 0
        self.keyMin = 1
        self.keyMax = 10000
        self.key = random.randint(self.keyMin, self.keyMax)
        self.min1 = 1
        self.min2 = 100
        self.min3 = 1
        self.max1 = 100
        self.max2 = 1
        self.max3 = 100
        self.weight1 = random.uniform(self.min1, self.max1)
        self.weight2 = random.uniform(self.min2, self.max2)
        self.weight3 = random.uniform(self.min3, self.max3)
        self.weights = [self.weight1, self.weight2, self.weight3]

    def returnWeights(self):
        return self.weights

    def checkState(self, player):
        self.notAlive = player.collisionDetect
        if(self.notAlive):
            self.aiScore = player.score
            return True
        else:
            return False

    def run(self, player, block1, block2, block3):
        if player.notDead:
            self.playerSpeed = block1.speed
            if(player.grounded):
                self.onGround = 1
            else:
                self.onGround = 0
            if(block1.xPos < block2.xPos and block1.xPos < block3.xPos):
                self.nextBlockPos = block1.xPos
            elif(block2.xPos < block1.xPos and block2.xPos < block3.xPos):
                self.nextBlockPos = block2.xPos
            else:
                self.nextBlockPos = block3.xPos
            self.blockDist = self.nextBlockPos - player.dinoRect.right

            # hidden nodes
            self.modOut1 = (self.blockDist * self.weight1) + (self.playerSpeed * self.weight2) + (self.onGround * self.weight3)
            self.modOut2 = (self.blockDist * self.weight1) + (self.playerSpeed * self.weight2) - (self.onGround * self.weight3)
            self.modOut3 = (self.blockDist * self.weight1) - (self.playerSpeed * self.weight2) + (self.onGround * self.weight3)

            # output layer
            self.finalOutput = self.modOut1 - self.modOut2 + self.modOut3
            if(self.finalOutput < self.key):
                self.finalOutput = 1
            else:
                self.finalOutput = 0

class learningModule():
    def __init__(self):
        self.oldMods = [
            [0,0,0,0,0]
            [0,0,0,0,0]
            [0,0,0,0,0]
            [0,0,0,0,0]
            [0,0,0,0,0]
        ] #TODO: Fix 2d array that will be used to read from a .txt
        temp1[5];
        for i in range(5):
            tempString = openFile.readline(i)
            for j in range(5):
                temp1(k) = tempString(0, tempString.find(" "))
                self.oldMods(i, j) = int(temp1(k))

    def improveNodes(self, aiList):
        #TODO: make some algorithm to determine the new range
        #Below is a makeshift temporary solution
        temp = "i"

block1 = enemy(1000)
block2 = enemy(1400)
block3 = enemy(1800)
blocks = [block1, block2, block3]
delay = 100
currentScore = 0
blocks[0].speed = 10
blocks[1].speed = 10
blocks[2].speed = 10
player = controller()
player1 = controller()
player2 = controller()
player3 = controller()
player4 = controller()
playerList = [player, player1, player2, player3, player4]
ai1 = ai()
ai2 = ai()
ai3 = ai()
ai4 = ai()
ai = ai()
aiList = [ai, ai1, ai2, ai3, ai4]
learningModule = learningModule()

def reset():
    global delay
    global blocks
    global currentScore
    currentScore = 0
    block1 = enemy(1000)
    block2 = enemy(1400)
    block3 = enemy(1800)
    blocks = [block1, block2, block3]
    delay = 100
    blocks[0].speed = 10
    blocks[1].speed = 10
    blocks[2].speed = 10

class scoreThread(threading.Thread):
    def __init__(self, Name, ID):
        threading.Thread.__init__(self)
        self.Name = Name
        self.ID = ID
    def run(self):
        print("working")
        scoreCounter(blocks[0], blocks[1], blocks[2], playerList, delay)

def main():
    score = scoreThread("thread1", 1)
    score.start()
    while True:
        screen.fill((245, 245, 245))
        # paints over entire screen, effectively clears screen

        # exit loop: checks for exit conditions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
                
        print("check collision")
        if player.collisionDetect(blocks) and player.notDead:
            openFile.write(str(ai.weights[0]) + " " + str(ai.weights[1]) + " " + str(ai.weights[2]) + " " + str(ai.key) + " " + str(ai.aiScore))
            player.delete()
        if player1.collisionDetect(blocks) and player1.notDead:
            openFile.write(str(ai1.weights[0]) + " " + str(ai1.weights[1]) + " " + str(ai1.weights[2]) + " " + str(ai1.key) + " " + str(ai1.aiScore))
            player1.delete()
        if player2.collisionDetect(blocks) and player2.notDead:
            openFile.write(str(ai2.weights[0]) + " " + str(ai2.weights[1]) + " " + str(ai2.weights[2]) + " " + str(ai2.key) + " " + str(ai2.aiScore))
            player2.delete()
        if player3.collisionDetect(blocks) and player3.notDead:
            openFile.write(str(ai3.weights[0]) + " " + str(ai3.weights[1]) + " " + str(ai3.weights[2]) + " " + str(ai3.key) + " " + str(ai3.aiScore))
            player3.delete()
        if player4.collisionDetect(blocks) and player4.notDead:
            openFile.write(str(ai4.weights[0]) + " " + str(ai4.weights[1]) + " " + str(ai4.weights[2]) + " " + str(ai4.key) + " " + str(ai4.aiScore))
            player4.delete()
        if not player.notDead and not player1.notDead and not player2.notDead and not player3. notDead and not player4.notDead:
            break

        #     if player.grounded and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #         player.jump()

        # AI logic, decides when AI jumps
        ai.run(player, block1, block2, block3)
        ai1.run(player1, block1, block2, block3)
        ai2.run(player2, block1, block2, block3)
        ai3.run(player3, block1, block2, block3)
        ai4.run(player4, block1, block2, block3)
        if(ai.finalOutput == 1):
            player.jump()
        if(ai1.finalOutput == 1):
            player1.jump()
        if(ai2.finalOutput == 1):
            player2.jump()
        if(ai3.finalOutput == 1):
            player3.jump()
        if(ai4.finalOutput == 1):
            player4.jump()

        # Draws all objects onto the screen
        for i in blocks:
            i.update()
        for i in playerList:
            i.update(blocks)
        # Handles Score text
        scoreText = scoreFont.render(str(currentScore), False, (0, 0, 0))
        screen.blit(scoreText, (1, 1))

        # not completely sure what this does kek, I think it's for double buffers
        # TODO: does anyone wanna confirm this lol?
        pygame.display.flip()
        # this updates graphics, pygame is buffered and switches around buffers
        pygame.time.wait(40)
        # this limits game to ?? updates/sec

if __name__ == "__main__":
    main()
    pygame.display.quit()
    sys.exit()