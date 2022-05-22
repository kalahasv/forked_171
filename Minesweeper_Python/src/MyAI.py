# ==============================CS-199==================================
# FILE:         MyAI.py
#
# AUTHOR:       Justin Chung# ==============================CS-199==================================
# FILE:         MyAI.py
#
# AUTHOR:       Justin Chung
#
# DESCRIPTION:  This file contains the MyAI class. You will implement your
#               agent in this file. You will write the 'getAction' function,
#               the constructor, and any additional helper functions.
#
# NOTES:        - MyAI inherits from the abstract AI class in AI.py.
#
#               - DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
 
from http.client import FOUND
from re import A
from socket import if_indextoname

from AI import AI
from Action import Action
import numpy as np
import random
import time
 
 
class MyAI( AI ):
 
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
 
        self.initalCoords = [startX,startY]
        self.row = rowDimension
        self.col = colDimension
        self.numOfMines = totalMines
        self.numOfFlag = 0 #should be one by the end
        self.numUncoveredtiles = 1
        #self.unTiles = []
        #self.flag = []
 
        ### New Attempt
        # there are 3 type of tiles
 
        ## 1. Uncovered tile
        ## 2. flagged tile
        ## 3. untouched tile
 
        self.label = np.full((rowDimension, colDimension), -1)
        self.elabel = np.full((rowDimension, colDimension), -1)
        self.refLabel = np.full((rowDimension, colDimension), '') # this creates a reference board, an empty string indicates the tile has not been touched yet
        # we can label each tile as a flagged and uncovered

       
        self.amove = Action(AI.Action.UNCOVER, startX, startY) #uncovers the first move tile
        self.refLabel[startX, startY] = 'U'
        
        self.moves = [] # list all actions to do
        self.solvable = False
        self.p = 0 # probability of a mine 
        self.time_elapsed = 0.0

       
 
       
 
       # no prints this time
 
        ########################################################################
        #                           YOUR CODE ENDS                             #
        ########################################################################
 
       
    def getAction(self, number: int):
 
        #Note: The max time I'm putting rn is arbitrary since idk how much time there really is
        MAX_TIME = 1000
        remaining_time = MAX_TIME - self.time_elapsed
 
        if(remaining_time < 3):
            random_coords = self.chooseRandom()
            #print("hi")
            
        
        else:
            #print("Action start!")
            ts = time.time()
        ########################################################################
        #                           YOUR CODE BEGINS                           #
        ########################################################################
       
            #win condition= uncovered all except one tile
            self.numTiles()
            
            if len(self.moves) == 0:
                if (self.row * self.col) - self.numOfMines == self.numUncoveredtiles:
                    #print('Done')
                    return Action(AI.Action.LEAVE)

            #check which tiles are uncovered relative to the current position
            #uncovered = [] #tiles uncovered relative to start position
           
            if number != -1: # if the number is non negative then we work on the board
 
                self.refLabel[self.amove.getX(), self.amove.getY()] = 'U' # u indicates uncovered
                self.label[self.amove.getX(), self.amove.getY()] = number # the number of adjacent bombs

 
            #print('number of uncovered')
            #print(self.numUncoveredtiles)
            self.ruleOfThumb()
            
            if self.solvable == False and self.numUncoveredtiles == 1:
                temp = self.applyOpeningProb()
                
                if temp == False: # the probability is worse, then select one randomly
                    self.chooseRandom()
                    
                    
                
            
            #if len(self.moves) == 0:
                #print('Tackle Frontier')
                #self.tackleFrontier()
            
            #print(len(self.moves))
            if len(self.moves) != 0:
                next_move = self.moves.pop()
                
                self.amove = next_move
            
                return next_move
            #if self.numUncoveredtiles < (self.row * self.col) - self.numOfMines:
                #self.rescan()

            if self.solvable == False or len(self.moves) == 0:
                #print('cannot do ROT')
                self.chooseRandom()
            
            #if len(self.moves) == 0:
                
                #if (self.row * self.col) - self.numOfMines == self.numUncoveredtiles:
                    #print('equal')
                    #return Action(AI.Action.LEAVE)
                
            
                
                
            
                
            next_move = self.moves.pop()
                
            self.amove = next_move
            
            return next_move
                
            
 
           
 
 
 
 
 
 
       
       
       
        ########################################################################
        #                           YOUR CODE ENDS                             #
        ########################################################################
    def getSimpleProb(self): # probability of each tile being a bomb without prior knowledge
        n = self.numOfMines
        num = 0
        for x in range(self.row):
            for y in range(self.col):
                if self.refLabel == '':
                    num +=1
                    
        self.p = n / num
        
    
    def applyOpeningProb(self):
        num = self.label[self.amove.getX(), self.amove.getY()]
        
        if num / 8 < self.p: # uncover one of the random spots around the tile
            
            explore = self.getAdjacent(self.amove.getX(), self.amove.getY())
            coords = random.choice(explore)
            
            self.moves.append(Action(AI.Action.UNCOVER, coords[0], coords[1]))
            self.refLabel[coords[0], coords[1]] = 'U'
            
            return True
        else:
            return False
        
        
    def numTiles(self):
        num = 0
        for x in range(self.row):
            for y in range(self.col):
                if self.refLabel[x, y] == 'U':
                    num += 1
        #print(self.refLabel)
        self.numUncoveredtiles = num
        
        
    #def getFrontier(self, x, y):
        
        
    def tackleFrontier(self):
        temp_coords = []
        adj = []
        #print(self.row, self.col)
        #print(self.refLabel)
        for x in range(self.row):
            for y in range(self.col):
                if self.refLabel[x, y] == '': # find all the covered and unflag ones
                    temp_coords.append((x, y))
                    
        #print(temp_coords)
        
        
        if len(temp_coords) <= 8:
            
            for c in temp_coords:
                temp = self.getAdjacent(c[0], c[1]) # get all the adjacent nodes of the covered and unflag ones, make sure it is uncovered
                for y in temp:
                    if self.refLabel[y[0], y[1]] != '': 
                        adj.append(y)
            
            
        my_list = list(set(adj))
        
        
        
        #print(my_list)
        test = False
        for x in my_list:
            temp_adj = self.getAdjacent(x[0], x[1])
                
            noFlag = self.countNoFlag(temp_adj) # get all the number of no flags of the current move
            #yesFlag = self.countFlag(temp_adj) # get all the number of flags of the current move
            #print(noFlag)
            if self.elabel[x[0], x[1]] == 0: #  check if effective label == 0 
                #print('effect == 0')

                for i in temp_adj:
                    if self.refLabel[i[0], i[1]] == '':
                        self.moves.append(Action(AI.Action.UNCOVER, i[0], i[1]))
                        self.refLabel[i[0], i[1]] = 'U'
                        #self.numUncoveredtiles += 1
                test = True
            elif self.elabel[x[0], x[1]] == noFlag:
                #print('flaggging')
                for i in temp_adj:
                    if self.refLabel[i[0], i[1]] == '':
                        self.moves.append(Action(AI.Action.FLAG, i[0], i[1]))
                        self.refLabel[i[0], i[1]] = 'F'
                        
                    temporary = self.getAdjacent(x[0], x[1])
                
                    for x1 in temporary:
                        if self.refLabel[x1[0], x1[1]] != '':
                            self.label[x1[0], x1[1]] -= 1
                test = True
            
        self.solvable = test
    
        
    def ruleOfThumb(self):
        #print('ROT')
        test = False
        #print(self.amove.getX(), self.amove.getY())
        adj = self.getAdjacent(self.amove.getX(), self.amove.getY()) # get all the adjacent of the current move
        noFlag = self.countNoFlag(adj) # get all the number of no flags of the current move
        yesFlag = self.countFlag(adj) # get all the number of flags of the current move
        
        ## effective label
        self.elabel[self.amove.getX(), self.amove.getY()] = self.label[self.amove.getX(), self.amove.getY()] - yesFlag
        #print(self.elabel)
        
        if self.elabel[self.amove.getX(), self.amove.getY()] == 0: # effective label  == 0
            #print('effective == 0')
            for x in adj:
                if self.refLabel[x[0], x[1]] == '':
                    
                    #print('undiscovered tile and now inserting')
                    self.moves.append(Action(AI.Action.UNCOVER, x[0], x[1]))
                    self.refLabel[x[0], x[1]] = 'U'
                    #self.numUncoveredtiles += 1
                 
            
            test = True    
        
        
        elif self.elabel[self.amove.getX(), self.amove.getY()] == noFlag: # effective label == #no flags
            #print('Flag')
            for x in adj:
                if self.refLabel[x[0], x[1]] == '':
                    
                    #print('undiscovered tile and now inserting')
                    self.moves.append(Action(AI.Action.FLAG, x[0], x[1]))
                    self.refLabel[x[0], x[1]] = 'F'
                    
                temporary = self.getAdjacent(x[0], x[1])
                
                for x1 in temporary:
                    if self.refLabel[x1[0], x1[1]] != '':
                        self.label[x1[0], x1[1]] -= 1
            test = True
        
        
        self.solvable = test
            
        
    def countFlag(self, coords):
        
        yesFlag = 0
        for x in coords:

                
            if self.refLabel[x[0], x[1]] == 'F':
                yesFlag +=1
                
        return yesFlag
    
    def countNoFlag(self, coords):
        noFlag = 0
        for x in coords:

                
            if self.refLabel[x[0], x[1]] == '':
                noFlag +=1
                
        return noFlag
    
        
    def getAdjacent(self, a, b):
        
        coords = [(x + a, y + b)
                  for x in range(-1, 2) for y in range(-1, 2)
                  if (x, y) != (0, 0)] # get all the adjacent

        temp = [pair for pair in coords
                if self.tileinBounds(pair[0], pair[1])] # return the valid adjacents
        
        my_list = list(set(temp))
        
        return temp
 
    #check if tile is in Bounds or not
    def tileinBounds(self, x, y):
        return (x >= 0 and x < self.row) and (y >= 0 and y < self.col)
            
        

    def chooseRandom(self):
       
       
 
        explore = []
        for x in range(0, self.row):
            for y in range(0, self.col):
                if self.refLabel[x, y] == '': # if empty string then we explore
                    explore.append((x, y))
                    
        #print(explore)
 
        coords = random.choice(explore)
        self.refLabel[coords[0], coords[1]] == 'U'
        self.moves.append(Action(AI.Action.UNCOVER, coords[0], coords[1]))
        
        #self.numUncoveredtiles += 1
        #self.action = Action(AI.Action.UNCOVER, randx, randy)
 
#
# DESCRIPTION:  This file contains the MyAI class. You will implement your
#               agent in this file. You will write the 'getAction' function,
#               the constructor, and any additional helper functions.
#
# NOTES:        - MyAI inherits from the abstract AI class in AI.py.
#
#               - DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
 
