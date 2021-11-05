import time
from time import perf_counter as clock
import math
import random
import pygame, sys
from pygame.locals import *
import numpy as np

pygame.init()

# Colors
LIME = [0,255,0]
BLUE = [0,0,255]
RED = [255,0,0]
MAROON = [128,0,0]
GREEN = [0,128,0]
NAVY = [0,0,128]
YELLOW = [255,255,0]
FUCHSIA = [255,0,255]
AQUA = [0,255,255]
OLIVE = [128,128,0]
PURPLE = [128,0,128]
TEAL = [0,128,128]
ORANGE = [255,120,0]
BLACK = [0,0,0]
WHITE = [255,255,255]
GRAY = [128,128,128]
SILVER = [192,192,192]
DGRAY = [64,64,64]

def GameOfLife():
    ## Create window ##
    size = [700,1000]
    height = size[0]
    width = size[1]
    DSURF = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Game Of Life')

    b = 1
    grain = 5  # Size of a box in pixels
    spawnChance = 97
    height1 = round(height/grain)
    width1 = round(width/grain)

    blockArray = []
##    lifeList = np.zeros((width1,height1),dtype=int)
    aliveCount = 0
    for i in range(b,width1-b):
        for j in range(b,height1-b):
            c = random.randrange(100)
            if c > spawnChance:
##                lifeList[i][j] = 1
                blockArray.append(lifeblock(i,j,True))
                aliveCount += 1
            else:
                blockArray.append(lifeblock(i,j))
    print("blockArray completed", aliveCount,len(blockArray),blockArray[100].x)

    # Assign Neighbors
    for m in range(len(blockArray)):
        blockArray[m].getNeighbors(blockArray,m)
        blockArray[m].splitNeighbors()
    print("Neighbors Assigned")

    # Draw
    for i in range(len(blockArray)):
        if blockArray[i].alive == True:
            bl = blockArray[i]
            pygame.draw.rect(DSURF,[255,255,0],(bl.x*grain,bl.y*grain,grain,grain))
    pygame.display.update()

    # Pause before starting
    pauseGame()
                
    time = 0
    while True:
        DSURF.fill(BLACK)
##        for i in range(b,width1-b):
##            for j in range(b,height1-b):
##                if lifeList[i,j] > 0:
##                    e = lifeList[i,j]
##                    if e > 5:
##                        e = 5
##                    pygame.draw.rect(DSURF,[255,255,0],(i*grain,j*grain,grain,grain),0)
        aliveCount = 0
        for i in range(len(blockArray)):
            if blockArray[i].alive == True:
                aliveCount += 1
                bl = blockArray[i]
                pygame.draw.rect(DSURF,[255,255,0],(bl.x*grain,bl.y*grain,grain,grain))
        
        pygame.display.update()


        for j in range(len(blockArray)):
            blockArray[j].reset()
        for k in range(len(blockArray)):
            blockArray[k].tellNeighbors()
        for n in range(len(blockArray)):
            blockArray[n].symTest()
        for l in range(len(blockArray)):
            blockArray[l].iterateBlock()

        
##        lifeListNew = np.zeros((width1,height1),dtype=int)
##
##        for i in range(b,width1-b):
##            for j in range(b,height1-b):
##                s = s_number(lifeList,i,j)
##                if time > 200 and s != 0:
##                    print(s)
##                    pauseGame(0.01)
##                t = symmetryTest(lifeList,i,j)
##                if t == True and s > 0:
##                #if t == True:
##                    #lifeListNew[i,j] += 1
##                    lifeListNew[i,j] = 1
##                if s > 4 or s < 2: #Any cell dies
##                    if lifeList[i,j] > 0:
##                        lifeListNew[i,j] = lifeList[i,j] - 1
##                elif s == 3: #Any cell thrives
##                    lifeListNew[i,j] = lifeList[i,j] + 30
##                elif lifeList[i,j] == 1: #Remaining cells live
##                    lifeListNew[i,j] = lifeList[i,j]
####                p0 = random.randrange(10000)
####                if p0 == 42 and lifeListNew[i,j] == 1:
####                    lifeListNew[i,j] += 1
##                    
####                if s == 2:
####                    p1 = random.randrange(10000)
####                    if p1 > 9998:
####                        lifeListNew[i,j] = 1
####                p2 = random.randrange(1000)
####                if p2 > 1000 and s == 1:
####                    lifeListNew[i,j] = 1
##        lifeList = lifeListNew
        for event in pygame.event.get():
            if event.type == QUIT: # Quit function
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pauseGame()

        pygame.display.set_caption('Game Of Life - ' + str(time))
        time += 1
        #pauseGame()
##        if time == 200:
##            print(lifeList)


def s_number(lifeList,i,j):
    #g = random.choice([1,2])
    g = 1
    pop = 0
##    for k in range(-1,1):
##        for l in range(-1,1):
##            if k != 0 or l != 0:
##                pop += lifeList[i+k,j+l]
    for k in [-g,0,g]:
        for p in [-g,0,g]:
            pop += math.ceil(lifeList[i+k,j+p]/(lifeList[i+k,j+p]+5))
    pop -= lifeList[i,j]
    return pop
    
def symmetryTest(lifeList,i,j):
    if lifeList[i,j+1] == lifeList[i,j-1] and lifeList[i+1,j] == lifeList[i-1,j] and lifeList[i-1,j-1] == lifeList[i+1,j+1] and lifeList[i-1,j+1] == lifeList[i+1,j-1]:
        return True
    else:
        return False

def pauseGame(time = 0):
    a = clock()
    while True:
        if time != 0:
            b = clock() - a
            if b > time:
                return
        for event in pygame.event.get():
            if event.type == QUIT: # Quit function
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_m:
                    return
                if event.key == K_p:
                    pauseGame()


class lifeblock:
    #__slots__ = ['x','y','alive','neighborCount','neighbors','lifeNum','neighborsa','neighborsb']
    def __init__(self,x,y,alive = False):
        self.x = x
        self.y = y
        self.alive = alive
        self.neighborCount = 0
        self.neighbors = []
        if self.alive == True:
            self.lifeNum = 1
        else:
            self.lifeNum = 0
        self.neighborsa = []
        self.neighborsb = []
        self.sym = False

    def iterateBlock(lb,schema = "Striver"):
        if schema == "Classic":
##            print(lb.neighborCount)
##            pauseGame(0.05)
            if lb.neighborCount >= 4 or lb.neighborCount < 2: #Any cell dies
                lb.alive = False
            elif lb.neighborCount == 3: #Any cell thrives
                lb.alive = True
        elif schema == "Maze":
            if lb.neighborCount > 4 or lb.neighborCount < 2: #Any cell dies
                lb.alive = False
            elif lb.neighborCount == 3: #Any cell thrives
                lb.alive = True
        elif schema == "Striver":            
            if lb.neighborCount == 3: #Any cell thrives
                lb.lifeNum += 30
            elif (lb.neighborCount < 2 or lb.neighborCount > 4) and lb.lifeNum > 0: #Any cell dies
                lb.lifeNum -= 1
            elif lb.sym == True and lb.neighborCount > 0:
                lb.lifeNum = 1
            else:
                lb.lifeNum = 0

            if lb.lifeNum <= 0:
                lb.alive = False
            else:
                lb.alive = True

    def reset(lb):
        lb.neighborCount = 0

    def getNeighbors(lb,blockArray,m):
        i = 1
        length = len(blockArray)
        for j in range(length):
            if m < 10: # If array is early, start from beginning
                b = blockArray[j]
            elif m > length-10: # If array is late, start from end
                b = blockArray[length-j-1]
            else: # If neither, look around location
                k = m + math.ceil(i*j/2)
                if k >= 0 and k < length:
                    b = blockArray[k]
                i *= -1
                
            if abs(b.x - lb.x) <= 1 and abs(b.y -lb.y) <= 1:
                if b.x - lb.x != 0 or b.y - lb.y != 0:
                    lb.neighbors.append(b)
            if len(lb.neighbors) >= 8:
                return
            
    def splitNeighbors(lb):
        for i in range(len(lb.neighbors) - 1):
            n1 = lb.neighbors[i]
            for j in range(len(lb.neighbors)-i-1):
                n2 = lb.neighbors[i+j+1]
                if n2.x - lb.x == lb.x - n1.x and n2.y - lb.y == lb.y - n1.y:
                    lb.neighborsa.append(n1)
                    lb.neighborsb.append(n2)
##                    print(n2.x, n2.y, lb.x, lb.y, n1.x, n1.y)
##                    pauseGame(0.01)
##                elif j >= len(lb.neighbors):
##                    break
                    
    def symTest(lb):
        lb.sym = True
        for i in range(len(lb.neighborsa)):
            if lb.neighborsa[i].lifeNum != lb.neighborsb[i].lifeNum:
                lb.sym = False
            
    def tellNeighbors(lb,schema = "Striver"):
        if schema == "Classic":
            if lb.alive == True:
                for i in range(len(lb.neighbors)):
                    lb.neighbors[i].neighborCount += 1
        elif schema == "Striver":
            for i in range(len(lb.neighbors)):
                lb.neighbors[i].neighborCount += math.ceil(lb.lifeNum/(lb.lifeNum+5))
            lb.neighborCount += math.ceil(lb.lifeNum/(lb.lifeNum+5)) - lb.lifeNum
            


GameOfLife()






















    
