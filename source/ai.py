#!/usr/bin/env python3
# shebang for linux/mac/unix users

import random
import game

class ai:
    def __init__(self, id):
        self.ID = id
        self.aiScore = 0
        self.alive = True
        self.quit = False
        self.playerSpeed = 0
        self.onGround = 1
        self.blockDist = 0
        self.nextBlockPos = 0
        self.modOut1 = 0
        self.modOut2 = 0
        self.modOut3 = 0
        self.finalOutput = 0
        self.key = 50
        self.min1 = 5
        self.min2 = 5
        self.min3 = 5
        self.max1 = 9
        self.max2 = 9
        self.max3 = 9
        self.hiddenMod1 = random.uniform(self.min1, self.max1)
        self.hiddenMod2 = random.uniform(self.min2, self.max2)
        self.hiddenMod3 = random.uniform(self.min3, self.max3)
        self.hiddenMods = [self.hiddenMod1, self.hiddenMod2, self.hiddenMod3]

    def returnMods(self):
        for i in range(3):
            print(self.hiddenMods[i])
        print(self.aiScore)

    def checkState(self, player):
        self.alive = player.aliveState
        if(not self.alive):
            self.aiScore = player.score
            return True
        else:
            return False

    def run(self, player, threadName, block1, block2):
        while(not self.quit):
            self.playerSpeed = speed
            if(player.isGrounded):
                self.onGround = 1
            else:
                self.onGround = 0
            if(block1.blockX < block2.blockX):
                self.nextBlockPos = block1.blockX
            else:
                self.nextBlockPos = block2.blockX
            self.blockDist = self.nextBlockPos  # - game.player.playerX

            # hidden nodes
            self.modOut1 = self.blockDist + self.playerSpeed + self.onGround
            self.modOut2 = self.blockDist - self.playerSpeed + self.onGround
            self.modOut3 = self.blockDist - self.playerSpeed - self.onGround

            # output layer
            self.modOut1 = self.modOut1 * self.hiddenMod1
            self.modOut2 = self.modOut2 * self.hiddenMod2
            self.modOut3 = self.modOut3 * self.hiddenMod3
            self.finalOutput = self.modOut1 - self.modOut2 - self.modOut3
            if(self.finalOutput < self.key):
                self.finalOutput = 1
            else:
                self.finalOutput = 0
            self.quit = self.checkState(player)
            if(self.quit):
                self.returnMods()
                quit()

class aiThread(threading.Thread):
    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.ThreadID = threadID
        self.ThreadName = threadName

    def run(self):
        ai.run(player, "aiThread", block1, block2)
