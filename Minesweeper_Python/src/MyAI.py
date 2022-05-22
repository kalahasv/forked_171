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
        self.frontier_covered = [] # list of all covered frontiers
        self.frontier_uncovered = set() # list 
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
            if len(self.moves) == 0:
                #print('get moves')
                self.find_moves() # get some moves
                
                if len(self.moves) == 0:   
                    
                    #print('cannot find any')
                    return Action(AI.Action.LEAVE)
                
            if len(self.moves) == 0 and len(self.frontier_uncovered) == 1:
                self.getSimpleProb()
                t = self.applyOpeningProb
                
                
                    
            
                    

                
            next_move = self.moves.pop()
                
            self.amove = next_move
            
            return next_move
                
            
 
           
 
 
 
 
 
 
       
       
       
        ########################################################################
        #                           YOUR CODE ENDS                             #
        ########################################################################
        
    def find_moves(self):
        
        #print(self.frontier_covered)
        #print(self.frontier_uncovered)
        while True:
            
            if len(self.moves) != 0: # has stuff to do
                #print('has stuff to do')
                
                return
            
            self.numTiles()
            if (self.row * self.col) - self.numOfMines == self.numUncoveredtiles: # goal
                
                #print('appending the end')
                self.moves.append(Action(AI.Action.LEAVE))
                return
            
            if len(self.frontier_covered) == 0: # frontier is empty
                
                
                self.scan() # find a move
                
                if len(self.frontier_covered) == 0 and len(self.moves) == 0: # if still cannot find a move do a random move
                    
                    
                    
                    #print('random')
                    self.chooseRandom()
                    
                    return
            
            coords = self.frontier_covered.pop()
            
            if self.refLabel[coords[0], coords[1]] == 'U':
                continue
            
            self.ruleOfThumb(coords[0], coords[1])
            
                
            
        
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
        
        adj = self.getAdjacent(self.amove.getX(), self.amove.getY())
        
        
        if num / len(adj) < self.p: # uncover one of the random spots around the tile
            
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
        
        
    def scan(self):
        for i in range(self.row):
            for j in range(self.col):
                
                if self.label[i, j] >=0:
                    self.ruleOfThumb(i, j)
                    
                
        
    def ruleOfThumb(self, x, y):
        #print('ROT')
        test = False
        #print(self.amove.getX(), self.amove.getY())
        adj = self.getAdjacent(x, y) # get all the adjacent of the current move
        noFlag = self.countNoFlag(adj) # get all the number of no flags of the current move
        yesFlag = self.countFlag(adj) # get all the number of flags of the current move
        
        ## effective label
        self.elabel[x, y] = self.label[x, y] - yesFlag
        
        #print(x, y)
        if self.label[x, y] < 0:
            #print('big oof')
            return
            
        
        if self.elabel[x, y] == 0: # effective label  == 0
            #print('effective == 0')
            for t in adj:
                if self.refLabel[t[0], t[1]] == '': # if untouched
                    
                    #print('undiscovered tile and now inserting')
                    self.moves.append(Action(AI.Action.UNCOVER, t[0], t[1]))
                    #self.refLabel[x[0], x[1]] = 'U'
                    #self.frontier_covered.append(x) # frontier covered around the 
                    #self.numUncoveredtiles += 1
                 
            
            test = True    
        
        
        elif self.elabel[x, y] == noFlag: # effective label == #no flags
            #print('Flag')
            for t in adj:
                if self.refLabel[t[0], t[1]] == '':
                    
                    #print('undiscovered tile and now inserting')
                    self.moves.append(Action(AI.Action.FLAG, t[0], t[1]))
                    self.refLabel[t[0], t[1]] = 'F'
                    
                temporary = self.getAdjacent(t[0], t[1])
                
                for x1 in temporary:
                    if self.refLabel[x1[0], x1[1]] != '':
                        self.elabel[x1[0], x1[1]] -= 1
            test = True
        
        else:
            #print('not done anything')
            return
        
        self.solvable = test
        
        for a in adj:
            if a not in  self.frontier_covered:
                self.frontier_covered.append(a) # get all the adjacents of the original adjacent as a frontier
        
        
        if self.refLabel[x, y] == 'U':
            self.frontier_uncovered.add((x, y))
    
    
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
 
