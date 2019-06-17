#!/usr/bin/env python3
import pygame
import sys
import threading
import random
import array
import math

pygame.init()
pygame.mixer.quit()
scoreFont = pygame.font.SysFont('Times New Roman', 14)
screen = pygame.display.set_mode((1000, 300))
groundHeight = 210
currentScore = 0
delay = 100
keyMin = 1
keyMax = 10000
min1 = 1
min2 = 1
min3 = 1
max1 = 1000
max2 = 1000
max3 = 1000
iteration = 0

class enemy(pygame.sprite.Sprite):
    global currentScore
    def __init__(self, beginPos):
        pygame.sprite.Sprite.__init__(self)
        self.xPos = beginPos
        self.image = pygame.image.load("./cacti.png")
        self.rect = self.image.get_rect()
        self.height = self.rect.bottom - self.rect.top
        self.rect = self.rect.move([beginPos, groundHeight])
        self.speed = 10
        self.minRandDist = 40
        self.maxRandDist = 150
        # the position the enemy begins at
        # when this block is spawned determines the position of the enemy
    def update(self):
        self.xPos -= self.speed
        self.rect = self.rect.move([-self.speed, 0])
        if self.xPos <= 0:
            self.randomDist = random.randint((self.speed * 10) + 0, (self.speed * 10) + 0)
            # TODO: NOTICE THE + 50 AND THE + 100 IN THE ABOVE LINE
            # WE CAN SHORTEN IT AS AI GETS GOOD
            # basically, the above line makes sure the dinosaur always has enough space to make the jump
            self.rect = self.rect.move([(1000 + self.randomDist) - self.xPos, 0])
            self.xPos = 1000 + self.randomDist
        if currentScore % 100 == 0:
            self.minRandDist += 20
            self.maxRandDist += 20
        # pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, (groundHeight + self.height), self.height, self.height))
    def draw(self):
        screen.blit(self.image, self.rect)

class controller(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.notDead = True
        self.yPos = groundHeight
        self.xPos = 50
        self.image = pygame.image.load("./dinosaur.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move([50, groundHeight])
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
        if enemy.rect.top <= self.rect.bottom - 20 and enemy.rect.left <= self.rect.right - 12:
                return True
        return False
    def collisionDetect(self, enemy):
        global exitFlag
        for i in enemy:
            if self.isTouching(i):
                return True
        return False
    def update(self):
        if self.notDead:
            # updates the player and draws it
            # also handles jump after it has been initiated
            if not self.grounded:
                self.yPos -= self.jumpIncrement
                self.rect = self.rect.move([0, -self.jumpIncrement])
                self.jumpIncrement -= 2
            if self.yPos >= 200:
                self.grounded = True
                self.rect.move([0, 200 - self.yPos])
                self.yPos = 200
            # pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, self.yPos, self.width, self.height))
            # pygame.draw.rect(screen, (65, 65, 65), pygame.Rect(self.xPos, self.yPos, self.width, self.height))
    def draw(self):
        screen.blit(self.image, self.rect)
    def delete(self):
        self.notDead = False

def scoreCounter(blocks, playerList, delay):  # add a delay variable
    global currentScore
    currentScore = 0
    while(True):
        currentScore += 1
        if currentScore <= 1000:
            if currentScore % 100 == 0:
                delay -= 10
                for i in blocks:
                    i.speed += 1
        else:
            if currentScore % 100 == 0:
                delay -= 5
                if delay < 5:
                    delay = 5
            counter = 0
            for i in playerList:
                if not i.notDead:
                    counter += 1
            if counter >= 5:
                sys.exit()
        pygame.time.wait(delay)

class ai:
    def __init__(self, keyMin, keyMax, min1, min2, min3, max1, max2, max3):
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
        self.keyMin = keyMin
        self.keyMax = keyMax
        self.min1 = min1
        self.min2 = min2
        self.min3 = min3
        self.max1 = max1
        self.max2 = max2
        self.max3 = max3
        self.key = random.randint(self.keyMin, self.keyMax)
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
    def reroll(self, keyMin, keyMax, min1, min2, min3, max1, max2, max3):
        self.keyMin = keyMin
        self.keyMax = keyMax
        self.min1 = min1
        self.min2 = min2
        self.min3 = min3
        self.max1 = max1
        self.max2 = max2
        self.max3 = max3
        self.key = random.randint(self.keyMin, self.keyMax)
        self.weight1 = random.uniform(self.min1, self.max1)
        self.weight2 = random.uniform(self.min2, self.max2)
        self.weight3 = random.uniform(self.min3, self.max3)
        self.weights = [self.weight1, self.weight2, self.weight3]
    def run(self, player, block1, block2, block3):
        global currentScore
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
            self.blockDist = self.nextBlockPos - player.rect.right

            # hidden nodes
            self.modOut1 = [(self.blockDist * self.weight1), (self.playerSpeed * self.weight2), (self.onGround * self.weight3)]
            self.modOut2 = [(self.blockDist * self.weight1), (self.playerSpeed * self.weight2), (self.onGround * self.weight3)]
            self.modOut3 = [(self.blockDist * self.weight1), (self.playerSpeed * self.weight2), (self.onGround * self.weight3)]

            # output layer
            self.finalOutput = self.modOut1[0] * ((self.modOut2[1]*self.modOut3[2])-(self.modOut2[2]*self.modOut3[1]))
            self.finalOutput += self.modOut1[1] * ((self.modOut2[0]*self.modOut3[2])-(self.modOut2[2]*self.modOut3[0]))
            self.finalOutput += self.modOut1[2] * ((self.modOut2[0]*self.modOut3[1])-(self.modOut2[1]*self.modOut3[0]))
            self.aiScore = currentScore
            if(self.finalOutput < self.key):
                self.finalOutput = 1
            else:
                self.finalOutput = 0

class learningModule():
    def __init__(self):
        self.oldMods = [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ] #TODO: Fix 2d array that will be used to read from a .txt
        self.inputArr = ["", "", "", "", ""]
        self.tempStr = ""
        self.tolerance = 500
    def getMods(self):
        readStream = open("weight_values.txt", "r")
        self.oldMods = []
        for i in range(5):
            tempString = readStream.readline(i)
            print (tempString)
            tempList = tempString.split()
            print (tempList)
            for j in tempList:
                j = j.strip()
                j = float(j)
            self.oldMods.append(tempList)
            print (self.oldMods[i])
        readStream.close()
    def evaluateTolerance(self, iteration):
        if iteration == 1:
            self.oldScore = 0
            for i in range(4):
                self.oldScore += self.oldMods[i][4]
            self.oldScore /= 5
        else:
            self.newScore = 0
            for i in range(4):
                self.newScore += self.oldMods[i][4]
            self.newScore /= 5
            difference = self.newScore - self.oldScore
            improvement = (1/10000000)*(difference**3)
            self.tolerance -= improvement
    def improveNodes(self, aiList):
        global keyMin, keyMax, min1, min2, min3, max1, max2, max3
        self.getMods()
        print (self.oldMods)
        print ("------------------------------------")
        print (keyMin, keyMax)
        print (min1, max2)
        print (min2, max2)
        print (min3, max3)
        print ("------------------------------------")
        #TODO: make some algorithm to determine the new range
        #Below is a finished solution (somewhat) I hope it works
        for i in range(5):
            for j in range(5):
                if self.oldMods[i][4] > self.oldMods[j][4]:
                    temp = self.oldMods[i]
                    self.oldMods[i] = self.oldMods[j]
                    self.oldMods[j] = temp
        acc = 0.35
        for i in range(5):
            acc -= 0.05
            for j in range(4):
                self.oldMods[i][j] *= acc
        for i in range(4):
            tempInt = 0
            for j in range(5):
                tempInt += self.oldMods[j][i]
            self.oldMods[1][i] = tempInt
        self.evaluateTolerance(iteration)
        self.newKeyMin = self.oldMods[0][3] - self.tolerance
        self.newKeyMax = self.oldMods[0][3] + self.tolerance
        keyMin = self.newKeyMin
        keyMax = self.newKeyMax

blocks = pygame.sprite.Group()
playerList = pygame.sprite.Group()
block1 = enemy(1000)
block2 = enemy(1400)
block3 = enemy(1800)
blocks.add(block1, block2, block3)
delay = 100
currentScore = 0
for i in blocks:
    i.speed = 10
player = controller()
player1 = controller()
player2 = controller()
player3 = controller()
player4 = controller()
playerList.add(player, player1, player2, player3, player4)
ai1 = ai(keyMin, keyMax, min1, min2, min3, max1, max2, max3)
ai2 = ai(keyMin, keyMax, min1, min2, min3, max1, max2, max3)
ai3 = ai(keyMin, keyMax, min1, min2, min3, max1, max2, max3)
ai4 = ai(keyMin, keyMax, min1, min2, min3, max1, max2, max3)
ai5 = ai(keyMin, keyMax, min1, min2, min3, max1, max2, max3)
aiList = [ai5, ai1, ai2, ai3, ai4]
ai5.reroll(keyMin, keyMax, min1, min2, min3, max1, max2, max3)
ai1.reroll(keyMin, keyMax, min1, min2, min3, max1, max2, max3)
ai2.reroll(keyMin, keyMax, min1, min2, min3, max1, max2, max3)
ai3.reroll(keyMin, keyMax, min1, min2, min3, max1, max2, max3)
ai4.reroll(keyMin, keyMax, min1, min2, min3, max1, max2, max3)
learningModule = learningModule()

def reset():
    global iteration
    global delay
    global blocks
    global currentScore
    global playerList
    global aiList
    iteration += 1
    currentScore = 0
    for i in playerList:
        i.notDead = True
    block1 = enemy(1000)
    block2 = enemy(1400)
    block3 = enemy(1800)
    blocks.empty()
    blocks.add(block1, block2, block3)
    delay = 100
    currentScore = 0
    for i in blocks:
        i.speed = 10
    for i in aiList:
        i.reroll(keyMin, keyMax, min1, min2, min3, max1, max2, max3)

class scoreThread(threading.Thread):
    def __init__(self, Name, ID):
        threading.Thread.__init__(self)
        self.Name = Name
        self.ID = ID
    def run(self):
        scoreCounter(blocks, playerList, delay)

def main(aiList, blocks, playerList, learningModule):
    score = scoreThread("thread1", 1)
    score.start()
    running = True
    while running:
        screen.fill((255, 255, 255))
        # paints over entire screen, effectively clears screen

        # exit loop: checks for exit conditions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        j = 0
        for i in playerList:
            if i.collisionDetect(blocks) and i.notDead:
                writeStream = open("weight_values.txt", "a")
                writeStream.write(str(aiList[j].weights[0]) + " " + str(aiList[j].weights[1]) + " " + str(aiList[j].weights[2]) + " " + str(aiList[j].key) + " " + str(aiList[j].aiScore))
                writeStream.close()
                print(str(aiList[j].weights[0]) + " " + str(aiList[j].weights[1]) + " " + str(aiList[j].weights[2]) + " " + str(aiList[j].key) + " " + str(aiList[j].aiScore))
                i.notDead = False
            j += 1

        if not player.notDead and not player1.notDead and not player2.notDead and not player3.notDead and not player4.notDead:
            reset()
            learningModule.improveNodes(aiList)
            writeStream = open("weight_values.txt", "w")
            writeStream.write("")
            writeStream.close()

        #     if player.grounded and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #         player.jump()

        # AI logic, decides when AI jumps
        ai5.run(player, block1, block2, block3)
        ai1.run(player1, block1, block2, block3)
        ai2.run(player2, block1, block2, block3)
        ai3.run(player3, block1, block2, block3)
        ai4.run(player4, block1, block2, block3)

        j = 0
        for i in playerList:
            if aiList[j].finalOutput == 1:
                i.jump()
            j += 1

        # Draws all objects onto the screen
        for i in blocks:
            i.update()
        for i in playerList:
            i.update()
        for i in blocks:
            i.draw()
        for i in playerList:
            i.draw()
        # Handles Score text
        scoreText = scoreFont.render(str(currentScore), False, (0, 0, 0))
        screen.blit(scoreText, (1, 1))

        pygame.display.flip()
        # this updates graphics, pygame is buffered and switches around buffers
        pygame.time.wait(17)
        # this limits game to 25 frames/sec

if __name__ == "__main__":
    main(aiList, blocks, playerList, learningModule)
    pygame.display.quit()
    sys.exit()
