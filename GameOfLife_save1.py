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

def GameOfLife(size):
    ## Create window ##
    height = size[0]
    width = size[1]
    DSURF = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Game Of Life')

    b = 2
    grain = 10  # Size of a box in pixels
    height1 = round(height/grain)
    width1 = round(width/grain)
    initPercent = 30

    lifeList = np.zeros((width1,height1),dtype=int)
    for i in range(b,width1-b):
        for j in range(b,height1-b):
            c = random.randrange(100)
            if c > initPercent:
                lifeList[i,j] = 1
                
    time = 0
    while True:
        DSURF.fill(BLACK)
        for i in range(b,width1-b):
            for j in range(b,height1-b):
                if lifeList[i,j] > 0:
                    e = 255 - lifeList[i,j]
                    if e < 0:
                        e = 0
                    pygame.draw.rect(DSURF,[255,255,255-e],(i*grain,j*grain,grain,grain),0)
        pygame.display.update()
        
        lifeListNew = np.zeros((width1,height1),dtype=int)

        for i in range(b,width1-b):
            for j in range(b,height1-b):
                s = s_number(lifeList,i,j)
                t = symmetryTest(lifeList,i,j)
##                if t == True:
##                    lifeListNew[i,j] = 1
                if s > 4 or s < 2: #Any cell dies
                    if lifeList[i,j] > 0:
                        lifeListNew[i,j] -= 1
                elif s == 3: #Any cell lives
                    lifeListNew[i,j] += 1
                elif lifeList[i,j] == 1: #Remaining cells live
                    lifeListNew[i,j] = 1
##                p0 = random.randrange(10000)
##                if p0 == 42 and lifeListNew[i,j] == 1:
##                    lifeListNew[i,j] += 1
                    
##                if s == 2:
##                    p1 = random.randrange(10000)
##                    if p1 > 9998:
##                        lifeListNew[i,j] = 1
##                p2 = random.randrange(1000)
##                if p2 > 1000 and s == 1:
##                    lifeListNew[i,j] = 1
        lifeList = lifeListNew
        for event in pygame.event.get():
            if event.type == QUIT: # Quit function
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pauseGame()

        pygame.display.set_caption('Game Of Life - ' + str(time))
        time += 1
        #pygame.time.delay(3)
        if time == 200:
            print(lifeList)


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

def pauseGame():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: # Quit function
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_m:
                    return



GameOfLife([500,800])






















    
